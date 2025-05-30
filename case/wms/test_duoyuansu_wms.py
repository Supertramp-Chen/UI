import pytest
# from pywinauto import Desktop
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.slide import slide
from common.imageColor import *
from common.yanzhengma_jiajian import calculate_equation
# from page.zhuifeng_pages.zhuifeng_index import zhuifeng_index_page
# from page.wms_pages.wms_elements import WmsElements
from config.conf import ConfigManager
import time
import csv
from common.image_identify import image_identify
# from common.file_upload import upload_files
from page.wms_pages.form_generate.form_gen import WmsElements
"""
test_pytest.fixture + 生成器yield   一起实现了前置启动，后置清理的 装饰器
"""

@pytest.fixture(scope='class', autouse=True)
def login_logout(drivers):
    """
    登陆操作：
        从常量文件中获取网址并且访问 
        创建WmsElements实例 对WMS页面元素操作
        从常量文件获取获取账号密码
    """
    drivers.get(ConfigManager.WMS_URL)
    form_gen = WmsElements(drivers)
    form_gen.username = ConfigManager.USERNAME
    form_gen.password = ConfigManager.PASSWORD
    form_gen.image_input = '2'

    form_gen.click_log_in_button()
    yield
    '''
    登出操作：
        通过创建的WmsElements实例 对wms页面进行操作
    '''
    form_gen.click_logout_icon()
    time.sleep(2)
    form_gen.click_logout_button()
    time.sleep(2)
    form_gen.click_sure_logout()
class TestSearch:
    @pytest.mark.mytest123
    def test_001(self, drivers):
        """
            在一个def用例里面，
            如果有一个assert执行失败，
            整个用例都会停下来，所以要将用例原子化一些
        """
        form_gen = WmsElements(drivers)
        form_gen.click_kucunanniu
        form_gen.click_kucunkanban
        time.sleep(5)
# //*[@id="app"]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr[1]/td[3]/div/span
# //*[@id="app"]/div/div[2]/section/div/div[2]/div[3]/table/tbody/tr[2]/td[3]/div/span
        # 测试定位多元素
        # form_gen.py里写 table_rows = PageElements(css_selector='.el-table__row')
        for row in form_gen.table_rows:
            # 打印第三列
            second_td = row.find_element(By.XPATH, './td[3]/div/span')
            second_td = row.find_element(By.XPATH, './td[3]')
            print(second_td.text)
            # print(row.text) #打印全部
