import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope='session', autouse=True)
def drivers():

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 开启无头模式
    # chrome_options.add_argument("--disable-gpu")  # 解决部分环境下的 bug
    # chrome_options.add_argument("--no-sandbox")  # 适用于 CI/CD
    # chrome_options.add_argument("--disable-dev-shm-usage")  # 解决 Docker 共享内存不足
    # chrome_options.add_argument("--window-size=1920,1080")  # 适配不同分辨率
    driver = webdriver.Chrome(options=chrome_options)  # ✅ 传入 options

    # driver = webdriver.Chrome()
    # driver.maximize_window()
    yield driver
    driver.quit()