#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from config.conf import ConfigManager
import time
import csv
import threading

from page.wms_pages.form_generate.form_gen import WmsElements

"""
test_pytest.fixture + 生成器yield   一起实现了和unittest的setup，teardown一样的前置启动，后置清理的装饰器
"""


@pytest.fixture(scope='function', autouse=True)
def open_baidu(drivers):
    drivers.get(ConfigManager.WMS_URL)
    yield
    # print("后置")

def read_csv_file(file_path):
    """生成器方式去读取csv里面的数据来做数据驱动测试，yield关键字来控制一行一行的读取字典里面的内容（字典里面的数据是隐形的，还未产生，就和奶糖盒子一样的道理）"""
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)  # 这是一个迭代器对象，把每次读取出来的数据都放到字典里面存起来，下面用一个for循环一次一次的去读取字典里面的数据，确保不会一次性将所有的数据读取到内存中。
        for row in reader:  # 如过下面没有生成器，那么这里直接全部数据都遍历一遍，如果有生成器就会卡住，一个一个来，接收到next方法才会读取下一行。
            yield row['username'], row['password']


@pytest.mark.login_test
@pytest.mark.parametrize('username, password', read_csv_file(r'data/data.csv'))
def test_001(drivers, username, password):
    form_gen = WmsElements(drivers)
    form_gen.username = username
    form_gen.password = password
    form_gen.image_input = '2'
    form_gen.click_log_in_button()
    time.sleep(5)
    assert form_gen.login_fail.text == "仓库管理系统"
