from selenium import webdriver
import pytest


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.implicitly_wait(20)
    yield driver
    # driver.quit()
    driver.close()
