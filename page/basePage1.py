#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 指定 Python 解释器路径，适用于 Linux/Unix 系统。
# 声明 Python 文件使用 UTF-8 编码，避免中文乱码。


from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
'''**写个basepage类重新封装元素定位操作 ：**

​      **_LOCATOR_MAP字典 + PageObject类封装webdriver + pageElemet封装元素定位**



​    **通过****描述符****实现：传入键值对就能定位到元素，对元素赋值就能实现输入框中输入字符串的操作**



​    ***input_account = PageElement(xpath\***

​    ***='//\*[@id="app"]/div/form/div[1]/div/div/input')\***

​    ***form_gen = WmsElements(drivers)\***

​    ***form_gen.input_account = “admin”\***



​    **1. PageElement类写个 __init__ 方法****接收键值对**

​    **2. _LOCATOR_MAP****字典****将传入的键转换成 Selenium 需要的 By 类型**

​    **3. 访问它form_gen.input_account触发pageElement的****get****方法里的findElement**

​       **__get__ 让 input_account 变成 find_element()，访问时自动查找元素**

​        **相当于driver.find_element(By.XPATH, "...")**



​    **1. 赋值的时候 触发 PageElement 的** **__set__** **方法**

​    **2. 然后调用** **__get__** **方法，找到 input_account 的 WebElement**

​    **3. 然后执行****send_keys** **把 "admin" 写到框里**

​       **__set__ 让 username = "admin" 变成 send_keys("admin")，赋值时自动输入**

​        **相当于element.send_keys("admin")**



​    **写页面元素的定位**'''
'''
封装 Selenium 的 WebDriver
不需要直接调用 find_element()
而是像操作普通对象的属性一样访问 UI 元素

PageObject 代表一个网页
PageElement 代表网页上的元素
'''
# Map PageElement constructor arguments to webdriver locator enums
'''
这个字典是一个 翻译器，用于 把字符串转换成 Selenium 需要的 By 定位方式
这样你在代码里只需要写 id='kw'，它会自动转换成 By.ID, 'kw'，简化写法。
'''
_LOCATOR_MAP = {
    'xpath': By.XPATH,
    'id': By.ID,
    'tag_name': By.TAG_NAME,
    'name': By.NAME,
    'css': By.CSS_SELECTOR,
    'class1': By.CLASS_NAME
}

'''
封装 存WebDriver ，PageElement 需要用它来查找元素
将 WebDriver 传入 PageObject，后续不再直接操作 driver 只需要操作 PageObject
'''
class PageObject(object):
    """
    接收driver，为了让driver后续完全脱手，再也不接触driver而写，
    让测试者能够摆脱driver的繁琐操作
    """

    def __init__(self, webdriver: object):
        """接收driver，为了让driver后续完全脱手，再也不接触driver而写，让测试者能够拜托driver的繁琐操作。"""
        self.w = webdriver

class PageElement(object):
    def __init__(self, context=False, **kwargs):
        # 保存定位信息，比如 xpath='//div'
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))  # 使用了迭代器，生成器来让(id='kw')变成By.id, 'kw'两个单独的参数
        self.locator = (_LOCATOR_MAP[k], v)
        self.has_context = bool(context)

    # 访问时自动调用 find_element()
    def __get__(self, instance, owner, context=None):
        """实现元素定位find_element()"""
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            context = instance.w

        return WebDriverWait(context, 5, 1).until(lambda x: x.find_element(*self.locator))

    # 赋值时自动执行 send_keys()
    def __set__(self, instance, value):
        """实现往元素中写入东西，send_keys()"""
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


class PageElements(object):
    """Page Element descriptor.

    :param accessibility_id:    `str`
        Use this accessibility_id locator
    :param xpath:    `str`
        Use this xpath locator
    :param ios_predicate:    `str`
        Use this ios_predicate locator
    :param uiautomator:    `str`
        Use this uiautomator locator
    :param uiautomation:    `str`
        Use this uiautomation locator

    :param context: `bool`
        This element is expected to be called with context

    Page Elements are used to access elements on a page. The are constructed
    using this factory method to specify the locator for the element.

                elem1 = PageElement(css='div.myclass')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(name='bar', context=True)

    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """

    def __init__(self, context=False, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))
        self.locator = (_LOCATOR_MAP[k], v)
        self.has_context = bool(context)

    def find(self, context):
        try:
            ele = WebDriverWait(context, 3, 1).until(lambda x: x.find_elements(*self.locator))
        except NoSuchElementException:
            return None
        except TimeoutException:
            return None
        else:
            return ele

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            context = instance.w

        return self.find(context)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


# Backwards compatibility with previous versions that used factory methods
page_element = PageElement
page_elements = PageElements
