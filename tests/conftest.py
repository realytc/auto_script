import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from configs import env_config
import datetime
import os
import sys
import stat

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages import register
from utils.logger import get_logger

logger = get_logger(__name__)
RegisterPage = register.RegisterPage


# 自動加執行權限
def pytest_addoption(parser):
    """添加 pytest 命令列選項"""
    parser.addoption(
        "--env",
        action="store",
        default="prod",
        help="Environment to use: uat or prod (default: prod)."
    )
    parser.addoption(
        "--device",
        action="store",
        default="desktop",
        help="Device mode to use: desktop, tablet, or mobile (default: desktop)."
    )


@pytest.fixture(scope="session")
def device(request):
    """回傳目前裝置模式"""
    return request.config.getoption("--device")

def configure_device_options(device: str, options: webdriver.ChromeOptions):
    """
    根據 device 參數設定 ChromeOptions
    """
    device = device.lower()

    if device == "desktop":
        # 桌面直接設 window size
        options.add_argument("--window-size=1920,1200")
    elif device == "tablet":
        # Tablet 用內建 iPad 模擬
        mobile_emulation = {"deviceName": "iPad"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    elif device == "mobile":
        # Mobile 用內建 iPhone X 模擬
        mobile_emulation = {"deviceName": "iPhone X"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    else:
        raise ValueError(f"Unknown device: {device}")

@pytest.fixture(scope="session")
def chrome_browser(device):
    """
    建立並回傳一個 Chrome 瀏覽器 WebDriver 實例。
    執行完後自動清理。
    """

    # 建立 ChromeOptions 物件
    options = webdriver.ChromeOptions()

    # Jenkins執行時建議啟用無頭模式
    # options.add_argument('--headless')

    # 常用穩定性參數
    options.add_argument('--no-sandbox')
    options.add_argument("--incognito")
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    # 根據 device 設定
    configure_device_options(device, options)

    # 自動下載 chromedriver
    driver_path = ChromeDriverManager().install()

    # 強制修正路徑
    if not os.path.basename(driver_path) == "chromedriver":
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver")
    print("使用的chromedriver路徑：", driver_path)

    # mac 自動加執行權限
    st = os.stat(driver_path)
    os.chmod(driver_path, st.st_mode | stat.S_IEXEC)

    chrome_service = Service(driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    yield driver

    driver.delete_all_cookies()
    driver.quit()

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")    
    

@pytest.fixture(scope="session")
def page_config(env, request):
    """
    通用 fixture，可依據測試中參數切換不同頁面設定
    """
    page = request.param
    return env_config[env][page]

@pytest.fixture(scope="session")
def register_page＿data(env):
    """
    專門取得 register 頁面的 URL 或其他資訊
    """
    return env_config[env]["register"]
@pytest.fixture(scope="session")
def register_test_data(register_page_data):
    """
    專門取得 register頁面的測試資料
    """
    return register_page_data["test_data"]


@pytest.fixture(scope="function")
def register_page(chrome_browser, env):
    """
    開啟 Register 頁面並返回 RegisterPage 實例
    """
    url = env_config[env]["register"]["url"]
    chrome_browser.get(url)
    logger.info(f"Opened register page: {url}")
    return RegisterPage(chrome_browser)

# tryfirst=True = 多個hook時，先跑這個 hook
# hookwrapper=True = 可以在執行前後插入代碼，攔截結果、修改結果，收集測試資訊
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    利用 pytest hook function 捕獲報錯並寫入 log 檔
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs('error_log', exist_ok=True)
        log_file = os.path.join('error_log', f"error_{now}.log")

        # 預設值
        error_message = ""
        error_path = ""
        error_lineno = ""

        # 根據型態分別處理
        if hasattr(report.longrepr, "reprcrash"):
            error_message = report.longrepr.reprcrash.message
            error_path = report.longrepr.reprcrash.path
            error_lineno = report.longrepr.reprcrash.lineno
        else:
            # 直接轉成字串
            error_message = str(report.longrepr)

        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"測試案例: {report.nodeid}\n")
            log.write(f"測試時間: {now}\n")
            log.write(f"錯誤訊息: {error_message}\n")
            if error_path:
                log.write(f"檔案路徑: {error_path}\n")
            if error_lineno:
                log.write(f"行號: {error_lineno}\n")
            log.write("=========================================\n")

