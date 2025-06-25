"""
AssertUtil.assert_equal(driver.title, "百度首页")
AssertUtil.assert_in("百度", driver.title)
AssertUtil.assert_true(button.is_displayed())
AssertUtil.assert_false(element.is_selected())
"""
class Assert:
    @staticmethod
    def assert_equal(actual, expected, msg=''):
        # 覆盖：
        # - 页面跳转断言 (assert driver.current_url == ...)
        # - 操作后页面标题断言 (assertEqual(actual_title, expected_title))
        # - 集合断言（验证表格行数等）
        assert actual == expected, msg or f"断言失败：实际值 [{actual}] 不等于预期值 [{expected}]"

    @staticmethod
    def assert_in(member, container, msg=''):
        # 文本匹配断言 (assert "百度" in driver.title)
        assert member in container, msg or f"断言失败：[{member}] 不在 [{container}] 中"

    @staticmethod
    def assert_true(expr, msg=''):
        # - 元素状态断言（按钮可见、可交互）
        #   (assert button.is_displayed(), assert button.is_enabled())
        # - 元素存在断言 (assert element is not None)
        # - 异常断言的成功分支（try-except里用 Assert.assert_true(True)）
        assert expr, msg or "断言失败：表达式不为True"

    @staticmethod
    def assert_false(expr, msg=''):
        # 覆盖：
        # - 按钮未选中断言 (assertFalse(element.is_selected()))
        # - 异常断言的失败分支 (比如 try 里面写 assert_false(True))
        assert not expr, msg or "断言失败：表达式不为False"

    @staticmethod
    def assert_greater(actual, expected, msg=''):
        # 覆盖：
        # - 数值比较断言 (assert value > 10)
        assert actual > expected, msg or f"断言失败：实际值 [{actual}] 不大于预期值 [{expected}]"