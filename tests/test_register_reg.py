from configs import env_config
import sys
import os

#確保找到檔案

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import requests
import time
import pages.register
from utils.logger import get_logger


logger = get_logger(__name__)   # __name__ 會顯示當前模組名稱

@pytest.fixture
def register_page_instance(chrome_browser):
    """
    創建 RegisterPage 實例的 fixture
    """
    return pages.register.RegisterPage(chrome_browser)

@pytest.fixture
def open_register_page(chrome_browser, register_page):
    """
    開啟 register 頁面
    """
    url = register_page["url"]
    chrome_browser.get(url)
    yield chrome_browser

@pytest.mark.parametrize("page_config", ["register"], indirect=True)
def test_open_register_page(chrome_browser, page_config):
    """
    嘗試使用共用性fixture，多個頁面需要測試開啟時，新增參數即可。
    """
    url = page_config["url"]
    chrome_browser.get(url)
    response = requests.get(url)
    logger.info(f"Already opend register page:: {url}.")

    # 檢查頁面是否開啟
    assert response.status_code == 200
    assert "ACY Securities Client Portal" in chrome_browser.title
    logger.info("Successfully opend register page.")

def test_country_selection_updates_mobile_code(chrome_browser, register_page_instance, register_data, open_register_page):
    # 在測試函數中創建 RegisterPage 實例，傳入 driver
    register = register_page_instance
    data = register_data
    expected_country_code = data['valid_data']['country_code']
    register.enter_country(data['valid_data']['country_of_residence'])
    actual_country_code = register.check_country_code()
        
    assert expected_country_code == actual_country_code, (
    f"Country code is not correct. "
    f"Expected: {expected_country_code}, Actual: {actual_country_code}"
)
    
    
    










