from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.logger import get_logger

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
        self.email_input = (By.NAME, "policy")
        self.privacy_policy_checkbox = (By.NAME, "policy")

    def enter_country(self, country:str):
        """
        輸入國家
        """
        country_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='country Select Input']"))
        )
        logger.info(f"Found element{country_field}, continue to input country")
        country_input = self.driver.find_element(*self.country_input)
        country_input.send_keys(country)
        country_input.send_keys(Keys.ENTER)
        logger.info(f"Input country: {country}")

    def check_country_code(self):
        """
        定位實際的國碼，並回傳國碼字串
        """
        WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located(self.country_code)
    )
        logger.info(f"Found element：{self.country_code}, continue to get country code")
        actual_country_code = self.driver.find_element(*self.country_code).get_attribute("value")
        logger.info(f"Found actual country code:：{actual_country_code}")
        return actual_country_code
    
    def enter_first_name(self, first_name:str):
        """
        待加上等待
        ACY Securities Client Portal" in chrome_browser.title
        這個元素出現，才能輸入
        """
        self.driver.find_element(*self.first_name_input).send_keys(first_name)



    def enter_mobile_number(self, mobile_number:str):
        """
        待加上等待
        ACY Securities Client Portal" in chrome_browser.title
        這個元素出現，才能輸入
        """
        self.driver.find_element(*self.phone_input).send_keys(mobile_number)
    
    def enter_email_address(self, email_address:str):
        """
        待加上等待
        ACY Securities Client Portal" in chrome_browser.title
        這個元素出現，才能輸入
        """
        self.driver.find_element(*self.email_input).send_keys(email_address)
    
    def enter_password(self, password:str):
        """
        待加上等待
        ACY Securities Client Portal" in chrome_browser.title
        這個元素出現，才能輸入
        """
    
        self.driver.find_element(*self.password_input).send_keys(password)
