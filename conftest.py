import pytest
from selenium import webdriver

@pytest.fixture(scope='session', autouse=True)
def drivers():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()