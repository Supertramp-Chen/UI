from page.basePage import PageObject, PageElement
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


class login_index_page(PageObject):
    input_account = PageElement(xpath='//*[@id="app"]/div/form/div[1]/div/div/input')
    input_password = PageElement(xpath='//*[@id="app"]/div/form/div[2]/div/div[1]/input')
    auto_code = PageElement(xpath='//*[@id="app"]/div/form/div[3]/div/div[1]/input')
    log_in_button = PageElement(xpath='//*[@id="app"]/div/form/div[4]/div/button[1]')
    # image = PageElement(id='app')
    # image = PageElement(src='data:image/gif;base64,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')
    # image_code = PageElement(xpath='//*[@id="app"]/div/form/div[3]/div/div[1]/input')


    @property
    def click_log_in_button(self):
        """点击搜索"""
        return self.log_in_button.click()



