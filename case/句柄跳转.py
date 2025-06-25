#
# driver.window_handles --获取所有窗口句柄 返回list
# driver.switch_to.window(handle)
#   handle=driver.window_handles[1]
# driver.current_window_handle
# driver.close() 关闭当前句柄
# driver.quit() 关闭浏览器

# 弹窗、iframe、句柄跳转，
# 用switch_to.alert、switch_to.frame、switch_to.window
# 再去定位该元素。