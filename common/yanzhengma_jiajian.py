def calculate_equation(equation):
    # 提取等式中的第二个字符
    operator = equation[1]

    # 提取表达式
    expression = equation[:3]

    # 根据运算符进行计算并得出结果
    if operator == "+":
        result = eval(expression)
        print(expression)
    elif operator == "-":
        result = eval(expression)
    elif operator == "*":
        result = eval(expression)
    elif operator == "/":
        result = eval(expression)
    else:
        result = None

    # 返回计算结果
    return result

print(calculate_equation("3+8=?"))