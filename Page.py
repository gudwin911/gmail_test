from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def scroll_down(self, num):
        self.driver.execute_script("window.scrollTo(0, %s);" % num)


class LogInPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get("https://www.google.com/gmail/about/#")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/nav/div/a[2]")))

    def to_sign_in(self):
        self.driver.find_element(By.XPATH, "/html/body/nav/div/a[2]").click()
        return SignInPage1(self.driver)

    def log_in(self, mail, password):
        return LogInPage(self.driver).to_sign_in().add_mail(mail).add_pass(password)


class SignInPage1(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[1]/input")))

    def past_mail(self, mail):
        field = self.driver.find_element(By.ID, "identifierId")
        field.send_keys(mail)
        return SignInPage1(self.driver)

    def next_btn(self):
        btn = self.driver.find_element(By.XPATH, "//div[2]/div[1]/div/content/span")
        btn.click()
        return SignInPage2(self.driver)

    def add_mail(self, mail):
        return SignInPage1(self.driver).past_mail(mail).next_btn()


class SignInPage2(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "password")))

    def past_pass(self, password):
        field = self.driver.find_element(By.NAME, "password")
        field.send_keys(password)
        return SignInPage2(self.driver)

    def next_btn(self):
        btn = self.driver.find_element(By.XPATH, "//div[2]/div[1]/div/content/span")
        btn.click()
        return InboxPage(self.driver)

    def add_pass(self, password):
        return SignInPage2(self.driver).\
            past_pass(password).\
            next_btn()


class InboxPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable
            ((By.XPATH, "//div[3]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div")))

    def click_new(self):
        btn = self.driver.find_element\
            (By.XPATH, "//div[3]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/div[1]/div/div")
        btn.click()
        return NewMailPage(self.driver)

    def create_new_mail(self, mail, subject, txt):
        return InboxPage(self.driver).\
            click_new().\
            add_mail(mail).\
            add_topic(subject).\
            add_text(txt).\
            send()

    def wait_for_email(self, mail):
        letters = self.driver.find_elements(By.CSS_SELECTOR, '[email*="%s"]' % mail)
        for letter in letters:
            if letter.is_displayed():
                letter.click()
                break
        return ReceivedMailPage(self.driver)


class NewMailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "subjectbox")))

    def add_mail(self, mail):
        field = self.driver.find_element(By.NAME, "to")
        field.send_keys(mail)
        return NewMailPage(self.driver)

    def add_topic(self, subject):
        field = self.driver.find_element(By.NAME, "subjectbox")
        field.send_keys(subject)
        return NewMailPage(self.driver)

    def add_text(self, txt):
        field = self.driver.find_element(By.CSS_SELECTOR, '[role*="textbox"]')
        field.send_keys(txt)
        return NewMailPage(self.driver)

    def send(self):
        field = self.driver.find_element(By.CSS_SELECTOR, '[data-tooltip*="Enter)"]')
        field.click()
        return InboxPage(self.driver)


class ReceivedMailPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_subject(self):
        subject = self.driver.find_element(By.CLASS_NAME, "hP")
        return subject.text

    def get_email_text(self):
        txt = self.driver.find_element(By.XPATH, "//div[1]/div[2]/div[3]/div[3]/div/div[1]")
        return txt.text

    def get_mail_data(self):
        subject = self.get_subject()
        txt = self.get_email_text()
        return subject, txt
