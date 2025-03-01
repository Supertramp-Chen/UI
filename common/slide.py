from selenium.webdriver import ActionChains


def slide(drivers, element, x, y):
    # ------------鼠标滑动操作------------
    action = ActionChains(drivers)
    # 第一步：在滑块处按住鼠标左键
    action.click_and_hold(element)
    # 第二步：相对鼠标当前位置进行移动
    action.move_by_offset(x, y)
    # 第三步：释放鼠标
    action.release()
    # 执行动作
    action.perform()
