from selenium.webdriver.common.by import By

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
        self.phone_input = (By.CSS_SELECTOR, "input.form-control.phone-input")
        self.password_input = (By.XPATH, "//input[@aria-label='register password input']")
        self.email_input = (By.NAME, "policy")
        self.privacy_policy_checkbox = (By.name, "policy")

    def enter_country(self, country:str):
        self.driver.find_element(*self.country_input).send_keys(country)

    def enter_first_name(self, first_name:str):
        self.driver.find_element(*self.first_name_input).send_keys(first_name)

    def enter_mobile_number(self, mobile_number:str):
        self.driver.find_element(*self.phone_input).send_keys(mobile_number)
    
    def enter_email_address(self, email_address:str):
        self.driver.find_element(*self.email_input).send_keys(email_address)
    
    def enter_password(self, password:str):
        self.driver.find_element(*self.password_input).send_keys(password)
