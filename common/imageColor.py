#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# ==================================================
# @Time : 2023-03-23 13:55:01
# @Author : 小北
# @微信：xiaobei_upup
# @Email : 2211484376@qq.com
# @QQ群：585971269
# @微信群：可加我微信拉你
# @Site : 苏州
# @Desc : 颜色识别工具类，元素截图工具函数
# @跳槽辅导：初中高级测试跳槽涨薪面试辅导，详情咨询微信
# @求职辅导：初中高级测试求职面试辅导，详情咨询微信
# @特色： 小北独创VIP面试速成课程，拿下心仪的offer
# ==================================================
"""
import cv2
import numpy as np
import collections
import os, random
import time
from PIL import Image
    

# pillow

def getColorList():
    """
    颜色范围初始化
    Returns:

    """
    # collections.defaultdict是一个字典子类，它在初始化时会指定默认的值类型。当你访问字典中不存在的键时，它会返回指定类型的默认值，而不是抛出KeyError异常。在这里，我们使用list作为默认值类型，所以当你访问dict中不存在的键时，它会返回一个空列表。
    dict = collections.defaultdict(list) # 创建一个字典，每一个字典的key对应的是一个list，等会在list中添加颜色的取值范围的数组就可以作为一种颜色了,dict内部是这样的数据结构 --> {“black” : "[array([  0,   0,   0]), array([180, 255,  55])]" }


    # 黑色
    lower_black = np.array([0, 0, 0])      # 固定写法，了解即可
    upper_black = np.array([180, 255, 55])  # 在HSV颜色空间中，H通道（色调）的取值范围是0到180，S通道（饱和度）的取值范围是0到255，V通道（亮度）的取值范围是0到55。
    color_list = []
    color_list.append(lower_black)  # 在list中将numpy数组添加到list的末尾
    color_list.append(upper_black)
    dict['black'] = color_list
    # print(dict['black'])  # 打印黑色的HSV空间的取值范围  输出[array([  0,   0,   0]), array([180, 255,  55])]

    # 灰色
    lower_gray = np.array([0, 0, 55])
    upper_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(upper_gray)
    dict['gray'] = color_list

    # 白色
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['white'] = color_list

    # 红色
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red'] = color_list

    # 红色2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red2'] = color_list

    # 橙色
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['orange'] = color_list

    # 黄色
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['yellow'] = color_list

    # 绿色
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list

    # 青色
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['cyan'] = color_list

    # 蓝色
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['blue'] = color_list

    # 紫色
    lower_purple = np.array([125, 43, 46])
    upper_purple = np.array([155, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['purple'] = color_list

    return dict


def get_color(image_path, shield_list=None):
    """
    获取指定图片的主体颜色，有且只会返回一种颜色
    函数解释：根据图像中与给定颜色字典中的颜色最匹配的区域来确定图像的主要颜色。它首先排除了在shield_list中指定的黑色颜色，然后对剩余的颜色进行比较，并找到面积最大的区域对应的颜色作为结果返回。如果没有找到符合条件的颜色，则返回None
    Args:
        image_path:待处理的图片路径
        shield_list: 需要屏蔽掉的颜色列表。
                    可选参数有'black'(黑色),'gray'(灰色),'white'(白色),'red'(红色),'red2'(红色2),'orange'(橙色),'yellow'(黄色),
                    'green'(绿色),'cyan'(青色),'blue'(蓝色),'purple'(紫色)

    Returns:    返回指定图片的主体颜色的字符串，例如'black'。如果是纯色图片，且该颜色被屏蔽，则返回None
    """
    if shield_list is None:
        shield_list = []  # 检测是否为none，如果是就置为空list，否则会报错
    image_frame = cv2.imread(image_path)   # 这是opencv库中的imread函数读取图像文件，然后加载到image_frame中
    hsv = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)  # 将RGB图像转换为HSV颜色空间，方便上述的color去对照
    maxsum = -100
    color = None
    color_dict = getColorList()  # 获取颜色字典大全
    for black_color in shield_list:
        if black_color in color_dict:
            color_dict.pop(black_color)  # 遍历是否有需要屏蔽的颜色，如果有就从字典中移除，后续识别过程中就会屏蔽该颜色
    tmp_num = random.randint(0, 99)
    color_dict_len = len(color_dict)
    same_pic = 0
    # 以下的循环是找到图片中颜色面积最大的颜色，作为返回结果，否则就none，不用详细记忆过程
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        # cv2.imwrite(os.path.join(tempfile.gettempdir(), f"{d}_{tmp_num}.jpg"), mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=0)
        cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum:
            maxsum = sum
            color = d
            same_pic = 1
        elif sum == maxsum:
            same_pic += 1
        if same_pic == color_dict_len:
            color = None

    return color


def get_screenshot_by_element(driver, element):
    """
    获取指定元素的截图(android/web通用)
    Args:
        driver: appium驱动 或者selenium驱动
        element: 要获取截图的元素

    Returns:

    """
    # 先截取整个屏幕/浏览器页面，存储至screenshots目录下
    TEMP_FILE = os.path.join("./screenshots", f"temp_screen_{int(time.time() * 1000)}.png")
    driver.get_screenshot_as_file(TEMP_FILE)

    # 获取页面上需要截图的元素的四角坐标
    location = element.location
    size = element.size

    # 截取具体目标元素的图片
    TEMP_FILE_2 = os.path.join("./screenshots", f"temp_screen_{int(time.time() * 1000)}.png")
    # 截取整张图片中的某一个目标元素的图片，并存到TEMP_FILE_2路径的screenshots目录下
    cut_image(TEMP_FILE, location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"],
              TEMP_FILE_2)
    return TEMP_FILE_2


def assert_color(driver, element):
    image_path = get_screenshot_by_element(driver, element)
    res = get_color(cv2.imread(image_path))
    if res == 'red' or res == 'red2':
        return 'red'
    elif res == 'green':
        return 'green'


def get_screenshot_by_percent(driver, out_image_path=None, x1=0, y1=0, x2=1, y2=1):
    """
    根据百分比截取屏幕截图
    Args:
        driver: appium驱动/webdriver驱动
        out_image_path: 截图结果输出路径
        x1: 所要截取区域左上角坐标的横坐标占屏幕宽度的百分比。0<=x1<=1
        y1: 所要截取区域左上角坐标的纵坐标占屏幕宽度的百分比。0<=y1<=1
        x2: 所要截取区域右上角坐标的横坐标占屏幕宽度的百分比。0<=x2<=1
        y2: 所要截取区域右下角坐标的纵坐标占屏幕宽度的百分比。0<=y2<=1

    Returns:截图结果存放路径

    """
    # 先截取整个屏幕，存储至系统临时目录下

    TEMP_FILE = os.path.join("./screenshots", f"temp_screen_{int(time.time() * 1000)}.png")
    driver.get_screenshot_as_file(TEMP_FILE)

    # 截取图片
    out_image_path = cut_image(TEMP_FILE, x1, y1, x2, y2, out_image_path, use_percent=True)
    return out_image_path


def cut_image(input_image_path, x1, y1, x2, y2, out_image_path, use_percent=False):
    """
    图片截取函数
    Args:
        input_image_path: 要处理的图片原始路径
        x1:要截取范围左上角的横坐标或百分比
        y1:要截取范围左上角的纵坐标或百分比
        x2:要截取范围右下角的横坐标或百分比
        y2:要截取范围右下角的纵坐标或百分比
        out_image_path: 结果输出的图片路径
        use_percent: 是否启用百分比模式，默认为不启用
    """
    if not out_image_path:
        out_image_path = os.path.join("./screenshots", f"temp_screen_{int(time.time() * 1000)}.png")
    image = Image.open(input_image_path)  # 读取原始图片
    if use_percent:
        size = image.size  # 获取图片的尺寸
        x1 = size[0] * x1
        y1 = size[1] * y1
        x2 = size[0] * x2
        y2 = size[1] * y2
    box = (x1, y1, x2, y2)  # 设定截取区域
    newImage = image.crop(box)  # 进行截取操作【这是核心函数，传入指定坐标就可以抠图】
    newImage.save(out_image_path)  # 保存截取结果
    return out_image_path


def get_color_by_element(driver, element, shield_list=None):
    """
    获取指定元素的主体颜色【常用】
    Args:
        driver: appium驱动
        element: 要获取颜色的元素
        shield_list: 要屏蔽的颜色列表
    Returns:

    """
    return get_color(get_screenshot_by_element(driver, element), shield_list)


if __name__ == '__main__':
    # filename = 'ios_h.png'
    # filename = 'C:\\Users\\viruser.v-desktop\\Desktop\\tmp\\white.png'
    # filename = 'D:\\img\\323232.png'

    filename = r"E:\Develop\Python\selenium_projects\xiaobei_selenium_automation\screenshots\blue.jpg"
    # filename = 'ios_l.png'
    # filename = 'and_h.png'
    # filename = 'and_l.png'
    print(get_color(filename, shield_list=['blue']))
    print(get_color(filename))
    # file_list = ['ios_h.png', 'ios_l.png', 'and_h.png', 'and_l.png']
    # for i in file_list:
    #     frame = cv2.imread(i)
    #     print(get_color(frame))
