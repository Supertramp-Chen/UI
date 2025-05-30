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
    # 填写登录时候的验证码
    # yzm = image_identify(drivers, form_gen.image, ConfigManager.WHOLE_PATH, ConfigManager.CROP_PATH)
    # form_gen.image_input = calculate_equation(yzm)
    form_gen.image_input = '2'

    # time.sleep(5)
    form_gen.click_log_in_button()
    yield
    '''
    登出操作：
        通过创建的WmsElements实例 对wms页面进行操作
    '''
    form_gen.click_logout_icon()
    time.sleep(2)
    # WebDriverWait(drivers, 5, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div'))
    form_gen.click_logout_button()
    time.sleep(2)
    form_gen.click_sure_logout()

    # form_gen.click_logout_icon()
    # form_gen.click_logout_button()
    # time.sleep(3)


class TestSearch:
    @pytest.mark.my
    def test_001(self, drivers):
        """
            在一个def用例里面，
            如果有一个assert执行失败，
            整个用例都会停下来，所以要将用例原子化一些
        """
        # global button
        # input1 = drivers.find_elements(By.CLASS_NAME, "el-input__inner")[0]
        # input1 = drivers.find_element(By.XPATH, '//*[@id="app"]/div/form/div[1]/div/div/input')
        # input1.send_keys(username1)
        # input2 = drivers.find_elements(By.CLASS_NAME, "el-input__inner")[1]
        # input2 = drivers.find_element(By.XPATH, '//*[@id="app"]/div/form/div[2]/div/div/input')
        # input2.send_keys(password1)
        # image = drivers.find_element(By.CLASS_NAME, "login-code-img")

        # login = drivers.find_elements(By.CLASS_NAME, "el-button")[0]
        # assert login.text == "登 录"
        # login.click()
        # assert login.is_displayed() == True

        # time.sleep(2)
        # zhufeng.image_code = image_identify(drivers, zhufeng.image,  '简单验证码.png', 'crop_pic.png')

        # churuku = drivers.find_elements(By.CLASS_NAME, "el-submenu__title")[2]
        # churuku.click()
        # ruku = drivers.find_element(By.CLASS_NAME, "el-menu-item")
        # ruku.click()
        # systemtool = drivers.find_elements(By.CLASS_NAME, "el-submenu__title")[4]
        # systemtool.click()

        # 单独创建 WmsElements 实例 在不同的测试流程中独立地获取页面元素
        form_gen = WmsElements(drivers)
        form_gen.click_system_tools()#搜索
        # print(get_color(get_screenshot_by_element(drivers, form_gen.system_tools), shield_list=['white']))
        # print(get_color(get_screenshot_by_element(drivers, form_gen.system_tools), shield_list=['white']))

        # ul = drivers.find_element(By.CLASS_NAME, "el-menu--inline")

        # li = ul.find_elements(By.TAG_NAME, "li")[0]
        # li = ul.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[1]/a')
        time.sleep(3)
        # 点击系统工具后的表单构建的li是否展示出来
        # assert form_gen.form_generate.is_displayed() == True
        # assert form_gen.form_generate.text == "表单构建"
        # assert form_gen.form_generate_icon.is_displayed() == True

        # assert form_gen.code_gen.is_displayed() == True
        # assert form_gen.code_gen.text == "代码生成"
        # assert form_gen.code_gen_icon.is_displayed() == True

        # assert form_gen.system_interface.is_displayed() == True
        # assert form_gen.system_interface.text == "系统接口"
        # assert form_gen.form_generate_icon.is_displayed() == True

        form_gen.click_form_generate()

        # assert form_gen.form_gen_logo.text == "Form Generator"

        form_gen.click_upload_element_button()

        # 断言文件上传按钮是蓝色
        # assert get_color(get_screenshot_by_element(drivers, form_gen.upload_button), shield_list=['white']) == "blue"
        assert get_color_by_element(drivers, form_gen.upload_button, shield_list=['white']) == "blue"

        # assert form_gen.upload_button.text == "点击上传"

        form_gen.click_upload_button()




        # upload_files(r'E:\Develop\Python\selenium_projects\xiaobei_selenium_automation\common\img.png')




        # upload = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[1]/div[2]/div[1]/div/div/div[4]/div[13]/div')
        # upload.click()

        # uploadbutton = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/div/div/button')
        # uploadbutton.click()

        # app = Desktop()
        # dialog = app['打开']
        # # 根据名字找到弹出窗口
        # dialog["Edit"].type_keys(r'E:\Develop\Python\selenium_projects\xiaobei_selenium_automation\common\img.png')
        # # 在弹出的框中输入相关的值。
        # dialog["Button"].click()

        # 对文件上传的图标断言
        # icon = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/div/div/button/i')
        # assert form_gen.upload_button_icon.is_displayed() == True

        # button_name = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/div/div/button/span')
        # assert button_name.text == "点击上传"

        # head_upload_name = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/label')
        # assert form_gen.upload_name.text == "上传"

        # 最后删除添加的各个组件
        # delete_icon = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/span[2]')
        # delete_icon.click()

        """
        form_gen.click_delete_upload()
        """

        # 判断文件上传组件是否删除
        # try:
        #     button = drivers.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div')
        # except NoSuchElementException:
        #     raise AssertionError(f"组件 {button} 不存在")  # 当一个用例里面出现了抛出异常的情况，那么def函数用例也会停止执行，一旦发现测试用例失败（包括断言失败、异常抛出等），pytest 将立即停止执行其他的测试用例，以减少不必要的运行时间。
        """
        slide(drivers, form_gen.upload_element_button, 300, 300)
        """

        # assert form_gen.upload_button.text == "点击上传"


    @pytest.mark.test
    def test_002_delete_upload(self, drivers):
        form_gen = WmsElements(drivers)
        form_gen.click_system_tools()
        form_gen.click_form_generate()
        # 对于input框的操作
        # input_phone_number = drivers.find_element(By.XPATH,
        #                                           '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[1]/div/div/div/input')
        # input_phone_number.send_keys("17205290079")
        # input_phone_number.clear()
        form_gen.input_phone_number = "17205290079"
        form_gen.input_phone_number.clear()

        # right_number = drivers.find_element(By.XPATH,
        #                                     '//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[1]/div/div/div/span[2]/span/span/span')
        assert form_gen.right_number.get_attribute("placeholder") == "请输入手机号"  # 获取input框中的默认提示语
        assert form_gen.right_number.text == "0/11"  # 这里有一个bug，由于电话号码都被clear清空了，后面的数据应该为0，而不是11，这里断言发现了一个bug，然后手动复现也是有这个bug的，然后就提bug了。
        # input_phone_number.send_keys("17205290078")
        form_gen.input_phone_number = "17205290078"
        form_gen.right_number.click()

        assert form_gen.right_number.text == "11/11"
        assert form_gen.input_phone_number.get_attribute(
            "value") == "17205290078"  # 对刚刚输入input框的str做断言，不能用text，因为是断言非用户输入的文本，后者是断言用户输入的文本，这里也可以在面试中如果被问道查看测试报告中的一些断言报错，就可以说这个。

    # @pytest.mark.test1
    # def test_002_webdriver_inner_methods(self, drivers):
    #     """
    #      webdriver 是driver身上的方法
    #         浏览器名称
    #         当前url
    #         当前页面标题
    #         当前页面源码 : drivers.page_source
    #         窗口句柄
    #         当前窗口所有句柄,是一个list
    #     """
    #     print(drivers.name, drivers.current_url, drivers.title,drivers.current_window_handle, drivers.window_handles)
    # drivers.back()
    # drivers.forward()
    # drivers.refresh()
    # 退出当前标签页
    # drivers.close()
    # 退出谷歌浏览器
    # drivers.quit()

    # def test_003_webelement_inner_methods(self, drivers):
    #     button_login = drivers.find_elements(By.CLASS_NAME, "el-button")[0]
    #     print(button_login.click(), button_login.text, button_login.is_displayed(), button_login.get_attribute('name'))
