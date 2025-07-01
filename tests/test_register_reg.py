import pages.register
from configs import env_config
import sys
import os

#確保找到檔案

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import requests
import time
from utils.logger import get_logger
from utils.error_msg import RegisterErrorＭsg



logger = get_logger(__name__)   # __name__ 會顯示當前模組名稱





@pytest.mark.parametrize("page_config", ["register"], indirect=True)
def test_open_register_page(register_page, page_config):
    """
    嘗試使用共用性fixture，多個頁面需要測試開啟時，新增參數即可。
    """
    url = page_config["url"]
    response = requests.get(url)
    # 檢查頁面是否開啟
    assert response.status_code == 200


def test_country_selection_updates_mobile_code(register_page, register_test_data):
    # 在測試函數中創建 RegisterPage 實例，傳入 driver

    data = register_test_data
    expected_country_code = data['valid_data']['country_code']
    register_page.enter_country(data['valid_data']['country_of_residence'])
    #檢查國碼
    actual_country_code = register_page.check_country_code()
        
    assert expected_country_code == actual_country_code, (
        f"Country code is not correct. "
        f"Expected: {expected_country_code}, Actual: {actual_country_code}"
    )
    logger.info("Country selection test passed")
    
def test_invalid_first_name(register_page, register_test_data):
    """
    測試無效的first name會顯示錯誤訊息
    """
    data = register_test_data
    register_page.enter_country(data['invalid_first_name']['country_of_residence'])
    register_page.check_country_code()
    register_page.enter_mobile_number(data['invalid_first_name']['mobile_number'])
    register_page.enter_email_address(data['invalid_first_name']['email_address'])
    register_page.enter_password(data['invalid_first_name']['create_password'])
    register_page.click_continue_button()
    assert register_page.check_invalid_first_name_error()
    
def test_first_name_over_40_chars(register_page, register_test_data):
    data = register_test_data
    register_page.enter_country(data['first_name_over_40_chars']['country_of_residence'])
    register_page.check_country_code()
    register_page.enter_mobile_number(data['first_name_over_40_chars']['mobile_number'])
    register_page.enter_email_address(data['first_name_over_40_chars']['email_address'])
    register_page.enter_password(data['invalid_last_name']['create_password'])
    register_page.click_continue_button()
    assert register_page.check_char_limit_first_name_error()

def test_invalid_last_name(register_page, register_test_data):
    data = register_test_data
    register_page.enter_country(data['invalid_last_name']['country_of_residence'])
    register_page.check_country_code()
    register_page.enter_mobile_number(data['invalid_last_name']['mobile_number'])
    register_page.enter_email_address(data['invalid_last_name']['email_address'])
    register_page.enter_password(data['invalid_last_name']['create_password'])
    register_page.click_continue_button()
    assert register_page.check_invalid_last_name_error()

def test_last_name_over_40_chars(register_page, register_test_data):
    data = register_test_data
    register_page.enter_country(data['last_name_over_40_chars']['country_of_residence'])
    register_page.check_country_code()
    register_page.enter_mobile_number(data['last_name_over_40_chars']['mobile_number'])
    register_page.enter_email_address(data['last_name_over_40_chars']['email_address'])
    register_page.enter_password(data['last_name_over_40_chars']['create_password'])
    register_page.click_continue_button()
    assert register_page.check_char_limit_last_name_error()









