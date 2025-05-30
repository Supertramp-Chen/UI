import pytest
from selenium import webdriver
from common.options_chrome import options1

'''装饰器+生成器 实现全局管理driver函数
测试用例和其他函数写了drivers作为参数 
    就获得yield driver返回的driver实例
不用手动创建和管理WebDriver对象的繁琐过程'''
'''
selemium 4.6之前 要手动下载chromedriver并加入环境变量
Selenium 4.6+ 版本 以后，不需要手动下载 ChromeDriver
	1.	你调用 webdriver.Chrome()
	2.	Selenium 检测你当前使用的是哪种浏览器（如 Chrome）
	3.	Selenium 内置的 Selenium Manager 被调用
	4.	Selenium Manager 执行以下动作：
	•	🔍 找到你本机的 Chrome 安装路径
	•	📌 获取 Chrome 浏览器版本号
	•	🌐 根据版本号从网络上下载对应版本的 chromedriver
	•	📦 下载后放到本地缓存目录（如：~/.cache/selenium）
	5.	Selenium 自动使用这个匹配好的 chromedriver 启动浏览器
	6.	你的自动化脚本开始运行 🎉
'''
''' 运行一次就执行一次
创建浏览器实例 + yield driver + 关闭浏览器'''
@pytest.fixture(scope='session', autouse=True)
def drivers():
    # driver = webdriver.Chrome()
    '''使用自定义的 启动参数来启动浏览器'''
    driver = webdriver.Chrome(options=options1())
    driver.maximize_window()
    yield driver
    driver.quit()


    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 开启无头模式
    # # chrome_options.add_argument("--disable-gpu")  # 解决部分环境下的 bug
    # # chrome_options.add_argument("--no-sandbox")  # 适用于 CI/CD
    # # chrome_options.add_argument("--disable-dev-shm-usage")  # 解决 Docker 共享内存不足
    # # chrome_options.add_argument("--window-size=1920,1080")  # 适配不同分辨率
    # # 创建浏览器实例
    # driver = webdriver.Chrome(options=chrome_options)  # ✅ 传入 options
    # yield driver
    # driver.quit()