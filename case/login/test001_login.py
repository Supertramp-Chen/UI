import pytest
from page.index_page.index import login_index_page
from config.conf import ConfigManager
import time
from common.image_identify import image_identify
"""
test_pytest.fixture + 生成器yield   一起实现了和unittest的setup，teardown一样的前置启动，后置清理的装饰器
"""
class TestSearch:
    @pytest.fixture(scope='function', autouse=True)
    def open_index(self, drivers):
        """打开百度"""
        drivers.get(ConfigManager.WMS_URL)
        yield
        print("后置wwwwwwwwwwwwww")

    @pytest.mark.test1
    @pytest.mark.parametrize('username, password', [
        ('wzz', '12345'),
        ('wzz2', '12345')
    ])
    def test_001(self, drivers, username, password):
        zhufeng = login_index_page(drivers)
        zhufeng.input_account = username
        zhufeng.input_password = password
        # zhufeng.log_in_button.click()
        # zhufeng.image_code = image_identify(drivers, zhufeng.image,  '简单验证码.png', 'crop_pic.png')
        zhufeng.click_log_in_button
        time.sleep(3)




if __name__ == '__main__':
    pytest.main(['vs', 'testcases/test_pytest/test_search_baidu_index.py'])
