#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Map PageElement constructor arguments to webdriver locator enums
"""Python 中，class 是一个保留关键字（reserved keyword），
用于定义类。如果在代码中直接使用 class 作为参数名，会导致语法错误"""
_LOCATOR_MAP = {
                'xpath': By.XPATH,
                'id': By.ID,
                'tag_name': By.TAG_NAME,
                'name': By.NAME,
                'css_selector': By.CSS_SELECTOR,
                'class1': By.CLASS_NAME
}
class PageObject(object):
    def __init__(self, webdriver: object, root_uri: object = None) -> object:
        self.w = webdriver
class PageElement(object):

    def __init__(self, context=False, **kwargs):
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        """使用迭代器，生成器来让(id='kw')变成By.id, 'kw'两个单独的参数"""
        k, v = next(iter(kwargs.items()))
        self.locator = (_LOCATOR_MAP[k], v)
        self.has_context = bool(context)

    def find(self, context):
        try:
            ele = WebDriverWait(context, 5, 1).until(lambda x: x.find_element(*self.locator))
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

# 等3秒，确保元素加载完，适合动态数据表（比如异步请求后表格）
# 表格多行、菜单列表
class PageElements(object):

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

# 不等，直接返回找到的所有行，适合静态数据表
# 如果表格在页面加载时就已经存在（而不是动态生成）
# 静态内容，多行
class MultiPageElement(PageElement):

    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


# Backwards compatibility with previous versions that used factory methods
page_element = PageElement
page_elements = PageElements
multi_page_element = MultiPageElement
