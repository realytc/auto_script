
import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.error_msg as error_msg
from pages.register import RegisterPage
import pytest
import requests
from utils.logger import get_logger



logger = get_logger(__name__)   # __name__ 會顯示當前模組名稱



def test_open_register_page(register_page, register_page＿data):
    """
    嘗試使用共用性fixture(page_config)，多個頁面需要測試開啟時，新增參數即可。
    """
    url = register_page＿data["url"]
    response = requests.get(url)
    # 檢查頁面是否開啟
    assert response.status_code == 200


def test_country_selection_updates_mobile_code(register_page, register_test_data):
    """
    測試國家輸入後是否更新手機號碼國碼
    """
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
    

@pytest.mark.parametrize(
    "data_key, error_check_method, expected_error_enum",
    [
        ("invalid_first_name", "check_invalid_first_name_error", error_msg.RegisterErrorMsg.INVALID_FIRST_NAME),
        ("first_name_over_40_chars", "check_char_limit_first_name_error", error_msg.RegisterErrorMsg.MAX_CHAR_LIMIT),
        ("invalid_last_name", "check_invalid_last_name_error", error_msg.RegisterErrorMsg.INVALID_LAST_NAME),
        ("last_name_over_40_chars", "check_char_limit_last_name_error", error_msg.RegisterErrorMsg.MAX_CHAR_LIMIT),
        ("invalid_email_address", "check_invalid_email_address_error", error_msg.RegisterErrorMsg.INVALID_EMAIL_ADDRESS),
    ],
    ids=[
        "Invalid First Name",
        "First Name >40 chars",
        "Invalid Last Name",
        "Last Name >40 chars",
        "Invalid Email Address"
    ]
)
def test_register_invalid_data(register_page, register_test_data, data_key, error_check_method, expected_error_enum):
    """
    測試無效資料組合會顯示正確的錯誤訊息
    """
    data = register_test_data
    old_url = register_page.driver.current_url
    logger.info(f"Old URL: {old_url}")

    # 將多筆的測試資料，抽出單筆資料
    record = data[data_key]

    # 輸入欄位
    register_page.refresh_page()
    register_page.enter_country(record["country_of_residence"])
    register_page.check_country_code()
    register_page.enter_first_name(record["first_name"])
    register_page.enter_last_name(record["last_name"])
    register_page.enter_mobile_number(record["mobile_number"])
    register_page.enter_email_address(record["email_address"])
    register_page.enter_password(record["create_password"])

    # 點擊繼續和URL變化檢查
    register_page.click_continue_button()
    
    new_url = register_page.driver.current_url
    logger.info(f"New URL: {new_url}")
    register_page.wait_for_url_change(old_url)

    # 執行對應的錯誤檢查
    error_check = getattr(register_page, error_check_method)
    actual_error_msg = error_check()
    # 取得錯誤訊息轉化為字串
    expected_error_msg = expected_error_enum.value

    assert actual_error_msg == expected_error_msg, (
        f"Expected error message: {expected_error_msg}, "
        f"Actual error message: {actual_error_msg}"
    )

def test_privacy_policy_redirect(register_page, register_test_data):
    old_url = register_page.driver.current_url
    original_window = register_page.driver.current_window_handle
    logger.info(f"original window: {original_window}")
    register_page.click_privacy_policy_redirect()
    new_window = register_page.driver.current_window_handle
    logger.info(f"new window: {new_window}")
    register_page.wait_for_new_tab_opened(original_window, old_url)
    register_page.switch_to_new_tab(original_window)
    new_window_url = register_page.driver.current_url
    logger.info(f"new window url: {new_window_url}")
    expected_url = register_test_data["privacy_policy_redirect"]["url"]
    logger.info(f"expected url: {expected_url}")
    assert new_window_url == expected_url, (
        f"New window url: {new_window_url}, "
        f"Expected url: {expected_url} ,"
    )








