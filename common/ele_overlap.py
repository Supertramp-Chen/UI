from selenium import webdriver


def check_overlap(component1, component2):
    driver = webdriver.Chrome()  # 初始化浏览器驱动，这里使用Chrome

    try:
        # 打开页面或者进行其他操作以加载组件
        # ...

        # 获取组件1的位置和大小
        location1 = component1.location
        size1 = component1.size
        x1, y1 = location1['x'], location1['y']
        width1, height1 = size1['width'], size1['height']

        # 获取组件2的位置和大小
        location2 = component2.location
        size2 = component2.size
        x2, y2 = location2['x'], location2['y']
        width2, height2 = size2['width'], size2['height']

        # 判断是否有重叠的地方
        if (x1 < x2 + width2 and x1 + width1 > x2 and
                y1 < y2 + height2 and y1 + height1 > y2):
            overlap = True
        else:
            overlap = False

        return overlap

    finally:
        driver.quit()  # 关闭浏览器驱动
