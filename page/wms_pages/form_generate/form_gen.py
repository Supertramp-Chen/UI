from page.basePage import *

"""
-------------------------------------------------
   File Name：
   Description :
   Author :   xiaobei
   CreateDate：
   wechat：xiaobei_upup
-------------------------------------------------
"""
"""
在平时中我们应该养成写注释的习惯，因为过一段时间后，没有注释，代码读起来很费劲。
"""


class WmsElements(PageObject):
    # 登录页面
    username = PageElement(xpath='//*[@id="app"]/div/form/div[1]/div/div/input')
    password = PageElement(xpath='//*[@id="app"]/div/form/div[2]/div/div/input')
    image = PageElement(class1='login-code-img')
    image_input = PageElement(xpath='//*[@id="app"]/div/form/div[3]/div/div[1]/input')
    login_button = PageElement(xpath='//*[@id="app"]/div/form/div[4]/div/button[1]')

    # 登出页面
    logout_icon = PageElement(xpath='//*[@id="app"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div/i')
    # logout_button = PageElement(class1='//*[@id="dropdown-menu-1380"]/li')  # 这里的xpath是定位不到的，不知道为啥，是一个无序列表中的li。
    logout_button = PageElement(class1="el-dropdown-menu__item--divided")  # 采用classname来定位，因为是唯一定位的。
    sure_logout = PageElement(xpath="/html/body/div[3]/div/div[3]/button[2]")
    dismiss_logout = PageElement(xpath='/html/body/div[3]/div/div[3]/button[1]')
    yes_or_no_logout_text = PageElement(xpath='/html/body/div[3]/div/div[2]/div[1]/div[2]/p')



    # 系统工具页面元素
    system_tools = PageElement(xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[1]/div[1]/div/div/div/div[1]/div')
    form_generate = PageElement(xpath='//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[1]/a/li')
    form_generate_icon = PageElement(
        xpath='//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[1]/a/li/svg/use')
    code_gen = PageElement(xpath='//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[2]/a/li')
    code_gen_icon = PageElement(xpath='//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[2]/a/li/svg')
    system_interface = PageElement(xpath='//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[3]/a/li')
    system_interface_icon = PageElement(
        xpath='//*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[8]/li/ul/div[3]/a/li/svg')

    # 表单构建页面
    form_gen_logo = PageElement(xpath='//*[@id="app"]/div/div[2]/section/div/div[1]/div[1]/div')
    upload_element_button = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[1]/div[2]/div[1]/div/div/div[4]/div[13]/div')
    upload_button = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/div/div/button')
    upload_button_icon = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/div/div/div/button/i')
    upload_name = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/div/label')
    delete_upload = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[2]/span[2]')

    input_phone_number = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[1]/div/div/div/input')
    right_number = PageElement(
        xpath='//*[@id="app"]/div/div[2]/section/div/div[2]/div[2]/div[1]/div/div/form/div[1]/div[1]/div/div/div/span[2]/span/span/span')

    # 登陆成功后的页面
    login_fail = PageElement(xpath='//*[@id="app"]/div/form/h3')

    def click_log_in_button(self):
        """点击搜索"""
        return self.login_button.click()

    def click_system_tools(self):
        """点击搜索"""
        return self.system_tools.click()

    def click_form_generate(self):
        """点击搜索"""
        return self.form_generate.click()

    def click_upload_element_button(self):
        """点击搜索"""
        return self.upload_element_button.click()

    def click_upload_button(self):
        """点击搜索"""
        return self.upload_button.click()

    def click_delete_upload(self):
        """点击搜索"""
        return self.delete_upload.click()

    def click_logout_icon(self):
        """点击搜索"""
        return self.logout_icon.click()

    def click_logout_button(self):
        """点击搜索"""
        return self.logout_button.click()

    def click_sure_logout(self):
        """点击搜索"""
        return self.sure_logout.click()

    def click_dismiss_logout(self):
        """点击搜索"""
        return self.dismiss_logout.click()
