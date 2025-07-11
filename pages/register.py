from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from utils.error_msg import RegisterErrorMsg
from utils.logger import get_logger

register_error_msg = RegisterErrorMsg
logger = get_logger(__name__)


class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.country_dropdown = (
            By.XPATH,
            "//label[contains(text(),'Country of Residence')]/following::div[@role='combobox']"
        )
        # 輸入框
        self.country_input = (
            By.XPATH,
            "//input[@aria-label='country Select Input']"
        )
        self.first_name_input = (By.NAME, "firstName")
        self.last_name_input = (By.NAME, "lastName")
        self.country_code = (
            By.CSS_SELECTOR,
            "input.form-control.phone-input"
        )
        self.phone_input = (
            By.CSS_SELECTOR,
            "input.form-control.phone-input"
        )
        self.password_input = (
            By.XPATH,
            "//input[@aria-label='register password input']"
        )
        self.email_input = (By.NAME, "email")
        self.privacy_policy_checkbox = (By.NAME, "policy")
        self.continue_button = (By.XPATH, "//button[@aria-label='continue button']")
        self.privacy_policy_redirect = (
        By.XPATH, '//a[@aria-label="Agree Policy Link" and contains(text(), "Privacy Policy")]')

    def refresh_page(self):
        """
        刷新當前頁面
        """
        self.driver.refresh()
        logger.info("Page refreshed.")

    def enter_country(self, country: str):
        """
        輸入國家
        """
        try:
            country_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='country Select Input']"))
            )
            logger.info(f"Found country input element: {country_field}")

            country_input = self.driver.find_element(*self.country_input)
            country_input.clear()
            country_input.send_keys(country)
            country_input.send_keys(Keys.ENTER)
            logger.info(f"Input country: {country}")

        except TimeoutException:
            logger.error(f"Timeout waiting for country input element")
            raise
        except Exception as err:
            logger.error(f"Error entering country {country}: {err}")

    def check_country_code(self):
        """
        定位實際的國碼，並回傳國碼字串
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.country_code)
            )
            logger.info(f"Found element：{self.country_code}, continue to get country code")
            actual_country_code = self.driver.find_element(*self.country_code).get_attribute("value")
            logger.info(f"Found actual country code:：{actual_country_code}")

        except Exception as err:
            logger.error(f"Error getting country code: {err}")

        return actual_country_code

    def enter_first_name(self, first_name: str):
        """
        輸入first_name
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.first_name_input)
            )
            first_name_input = self.driver.find_element(*self.first_name_input)
            first_name_input.clear()
            first_name_input.send_keys(first_name)
            logger.info(f"Input first name: {first_name}")
        except Exception as e:
            logger.error(f"Error entering first name {first_name}: {e}")

    def enter_last_name(self, last_name: str):
        """
        輸入last_name
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.last_name_input)
            )
            last_name_input = self.driver.find_element(*self.last_name_input)
            last_name_input.clear()
            last_name_input.send_keys(last_name)
            logger.info(f"Input last name: {last_name}")
        except Exception as e:
            logger.error(f"Error entering last name {last_name}: {e}")

    def enter_mobile_number(self, mobile_number: str):
        """
        輸入手機號碼
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.phone_input)
            )
            phone_input = self.driver.find_element(*self.phone_input)
            phone_input.clear()
            phone_input.send_keys(mobile_number)
            logger.info(f"Input mobile number: {mobile_number}")
        except Exception as e:
            logger.error(f"Error entering mobile number {mobile_number}: {e}")

    def enter_email_address(self, email_address: str):
        """
        輸入email地址
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.email_input)
            )
            email_input = self.driver.find_element(*self.email_input)
            email_input.clear()
            email_input.send_keys(email_address)
            logger.info(f"Input email address: {email_address}")
        except Exception as error:
            logger.error(f"Error entering email address {email_address}: {error}")

    def enter_password(self, password: str):
        """
        輸入密碼
        """

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.password_input)
            )
            password_input = self.driver.find_element(*self.password_input)
            password_input.clear()
            password_input.send_keys(password)
            logger.info(f"Input password: {password}")
        except Exception as error:
            logger.error(f"Error entering password: {error}")

    def click_continue_button(self):
        """
        點擊繼續按鈕
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.continue_button)
            )
            continue_button = self.driver.find_element(*self.continue_button)
            continue_button.click()
            logger.info("Clicked continue button...")
        except Exception as error:
            logger.error(f"Error clicking continue button: {error}")

    def wait_for_url_change(self, old_url):
        """
        等待 URL 變化
        """
        try:
            WebDriverWait(self.driver, timeout=10).until(
                EC.url_changes(old_url)
            )
            logger.info("URL changed successfully.")
        except TimeoutException:
            logger.error("Timeout waiting for URL to change.")

    def check_invalid_first_name_error(self):
        """
        檢查first name錯誤訊息
        """
        try:
            # 等待錯誤訊息出現
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@aria-label='Invalid Firstname' and contains(., register_error_msg.INVALID_FIRST_NAME)]"
                ))
            )
            error_text = error_element.text
            logger.info(f"Found first name error: {error_text}")
            return error_text

        except TimeoutException:
            logger.info("No first name error message found")
            return None
        except Exception as error:
            logger.error(f"Error checking first name error: {error}")

    def check_char_limit_first_name_error(self):
        """
        檢查first name字數超過40字錯誤訊息
        """
        try:
            # 等待錯誤訊息出現
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@aria-label='Invalid Firstname' and contains(., register_error_msg.MAX_CHAR_LIMIT)]"
                ))
            )
            error_text = error_element.text
            logger.info(f"Found first name error: {error_text}")
            return error_text
        except TimeoutException:
            logger.info("No first name error message found")
            return None
        except Exception as error:
            logger.error(f"Error checking first name error: {error}")

    def check_invalid_last_name_error(self):
        """
        檢查last name錯誤訊息
        """
        try:
            # 等待錯誤訊息出現
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@aria-label='Invalid Lastname' and contains(., register_error_msg.INVALID_LAST_NAME)]"
                ))
            )
            error_text = error_element.text
            logger.info(f"Found last name error: {error_text}")
            return error_text
        except TimeoutException:
            logger.info("No last name error message found")
            return None
        except Exception as error:
            logger.error(f"Error checking last name error: {error}")

    def check_char_limit_last_name_error(self):
        """
        檢查last name字數超過40字錯誤訊息
        """
        try:
            # 等待錯誤訊息出現
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@aria-label='Invalid Lastname' and contains(., register_error_msg.MAX_CHAR_LIMIT)]"
                ))
            )
            error_text = error_element.text
            logger.info(f"Found first name error: {error_text}")
            return error_text
        except TimeoutException:
            logger.warning("No first name error message found")
            return None
        except Exception as error:
            logger.error(f"Error checking first name error: {error}")

    def check_invalid_email_address_error(self):
        """
        檢查email address錯誤訊息
        """
        try:
            # 等待錯誤訊息出現
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//div[@aria-label='Invalid Email' and contains(., register_error_msg.INVALID_EMAIL_ADDRESS)]"
                ))
            )
            error_text = error_element.text
            logger.info(f"Found first name error: {error_text}")
            return error_text
        except TimeoutException:
            logger.warning("No first name error message found")
            return None
        except Exception as error:
            logger.error(f"Error checking first name error: {error}")

    def click_privacy_policy_redirect(self):
        """
        點擊 privacy policy 的文字連結
        """
        try:
            # 等待元素出現
            privacy_policy = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.privacy_policy_redirect)
            )
            logger.info(f"Found privacy policy element: {privacy_policy}")
            privacy_policy.click()
            logger.info(f"Clicked privacy policy")
        except TimeoutException:
            logger.warning("Timeout. Not found privacy policy")
            return None
        except Exception as error:
            logger.error(f"Found privacy policy element: {error}")

    def wait_for_new_tab_opened(self, original_handles, old_url):
        """
        等待新分頁開啟，回傳所有目前的 handles
        """
        logger.info(f"old url: {old_url}")
        WebDriverWait(self.driver, timeout=10).until(
            lambda d: len(d.window_handles) > len(original_handles) or d.current_url != old_url
        )
        return self.driver.window_handles

    def switch_to_new_tab(self, original_handles):
        """
        切換到新分頁 (會找出不是原始 handle 的那個)
        """
        try:
            for handle in self.driver.window_handles:
                if handle not in original_handles:
                    self.driver.switch_to.window(handle)
                    # 等新分頁載入
                    WebDriverWait(self.driver, timeout=10).until(
                        lambda d: d.current_url != "about:blank"
                    )
                    new_window_url = self.driver.current_url
                    logger.info(f"Switched to new tab: {new_window_url}")
                    return handle

        except Exception as error:
            logger.error(f"Switched to new tab error: {error}")

