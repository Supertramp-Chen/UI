#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    basePage
   Description :  Python descriptor
   Author :       beige
   CreateDate：   2023/03/19 21:36
-------------------------------------------------
功能：1、可以轻松实现元素定位
     2、还可以实现在某个元素输入字符串
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# Map PageElement constructor arguments to webdriver locator enums
_LOCATOR_MAP = {
    'xpath': By.XPATH,
    'id': By.ID,
    'tag_name': By.TAG_NAME,
    'name': By.NAME,
    'css': By.CSS_SELECTOR,
    'class1': By.CLASS_NAME
}


class PageObject(object):
    """
    接收driver，为了让driver后续完全脱手，再也不接触driver而写，
    让测试者能够拜托driver的繁琐操作。
                                    Page Object pattern.
    :param webdriver: `selenium.webdriver.WebDriver`
        Selenium webdriver instance
    :param root_uri: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
    """

    def __init__(self, webdriver: object):
        """接收driver，为了让driver后续完全脱手，再也不接触driver而写，让测试者能够拜托driver的繁琐操作。"""
        self.w = webdriver


class PageElement(object):
    """Page Element descriptor.
    :param xpath:    `str`
        Use this xpath locator
            elem1 = PageElement(css='div.myclass')
            elem2 = PageElement(id='foo')
    Page Elements act as property descriptors for their Page Object, you can get
    and set them as normal attributes.
    """

    def __init__(self, context=False, **kwargs):
        """处理传进来的元素定位键值对，让(id='kw')变成（By.id, 'kw'）"""
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        k, v = next(iter(kwargs.items()))  # 使用了迭代器，生成器来让(id='kw')变成By.id, 'kw'两个单独的参数
        self.locator = (_LOCATOR_MAP[k], v)
        self.has_context = bool(context)

    def __get__(self, instance, owner, context=None):
        """实现元素定位find_element()"""
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            context = instance.w

        return WebDriverWait(context, 5, 1).until(lambda x: x.find_element(*self.locator))

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
