import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from configs import env_config
import datetime
import re
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages import register
from utils.logger import get_logger


logger = get_logger(__name__)
RegisterPage = register.RegisterPage

import stat

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
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage') 

    # 根據device設置
    if device == "desktop":
        options.add_argument('--window-size=1920,1200')
    elif device == "tablet":
        options.add_argument('--window-size=800,1280')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1'
        )
    elif device == "mobile":
        options.add_argument('--window-size=375,812')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Mobile/15E148 Safari/604.1'
        )
    else:
        raise ValueError(f"Unknown device: {device}")

    # 建立 ChromeDriver 服務 (自動下載相容版本)
    # chrome_service = Service(executable_path=ChromeDriverManager().install())
    # 自動下載chromedriver
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
    本功能是利用pytest報告的hook function取出pytest報錯的log，
    並在error_log目錄下，建立.log檔。
    """
    # 暫停函數並返回一個結果容器，包含測試報告
    outcome = yield
    # 取得報告測試物件
    report = outcome.get_result()

    # 改為捕捉所有失敗（assert、Exception等）
    if report.when == 'call' and report.failed:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs('error_log', exist_ok=True)
        log_file = os.path.join('error_log', f"error_{now}.log")
        failed_txt = str(report.longrepr)
        
        """
        捕捉匹配到的兩個組合Failed結果的文字: 
        組合1： "Failed:" 與 "tests\" (末行的代碼行數)之間的所有字符。
        組合2： "tests\" 之後和 ": Failed" 之前的所有非空白字符。
        """
        path_sep = re.escape(os.sep) #設定 Windows(\) & Ubuntu(/) 的斜線通用辨識符號
        match = re.search(rf'Failed:(.*?)tests{path_sep}(\S+): Failed', failed_txt, re.DOTALL)

        if match:
            failed_msg_error = match.group(1).strip()
            failed_msg_code_line = match.group(2).strip()
            # 開檔模式為追加模式，避免覆蓋，編碼為utf-8
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"測試案例: {report.nodeid}\n")
                log.write(f"測試時間: {now}\n")
                log.write(f"報錯內容: {failed_msg_error}\n")
                log.write(f"程式詳情: {failed_msg_code_line}\n")
                log.write("=========================================\n")  # 添加分隔符或標記
        else:
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write("未找到匹配的錯誤資訊，或是其他預期外錯誤")
    else:
        pass
