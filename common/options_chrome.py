from selenium import webdriver
"""
    配置了浏览器的options会加快用例执行速度，
    所以这里的配置也是优化框架的一步
    配置和优化 Chrome 浏览器启动参数
"""
def options1():
    # 创建一个配置对象，用来设置浏览器启动选项（类似「启动命令行参数」）
    options = webdriver.ChromeOptions()

    # 页面加载策略
    # normal表示完全加载后再执行；还有eager和none
    options.page_load_strategy = 'normal'

    # 窗体最大化
    # 启动后自动最大化浏览器窗口
    options.add_argument('start-maximized')

    # 指定浏览器的启动坐标
    # options.add_argument('window-position=500,500')

    # 指定浏览器的窗体大小
    # options.add_argument('window-size=1200,800')

    # 去掉浏览器的自动化黄条：目前的阶段下已经不是那么有需要的了
    # 去掉「Chrome 正在被自动化软件控制」提示和日志干扰
    options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
    # options.add_experimental_option('disable-infobars')   # 只限于python2.7的版本有效，现在已经失效

    # 无头模式：不在桌面生成浏览器的运行，浏览器作为后台程序，静默后台运行。虽然无法肉眼看到，但实际上一切照旧，该运行的依旧会正常运行。可以减少测试设备的资源损耗。一般可用于持续集成中，虽然有可能出现错误。
    options.add_argument('--headless')

    # 去掉账号密码保存弹窗
    # 禁止 Chrome 弹出保存密码提示框
    prefs = {
        'credentials_enable_service': False,
        'profile.password_manager_enable': False
    }
    options.add_experimental_option("prefs", prefs)

    # 加载本地缓存信息：Selenium默认启动的浏览器是不会加载本地缓存的。
    # 载入本地浏览器用户数据，比如记住登录状态（用于绕过验证码/反爬）
    '''
        1. 该功能可以实现验证码的绕过，但前提条件是需要提前手动登录一次（只对可以记住登录状态的网站有效）。
        2. 该功能可以起到一定程度的反爬效果，具体根据被访问系统的反爬机制而决定
        3. 该功能的使用，只能够在一个浏览器生效，如果在启动之前开启有其他的chrome浏览器，则该功能无法生效，会报错。一定要关闭所有浏览器以后再运行webdriver
    '''
    # 自动化测试不会处理验证码，因为验证码本身就是防止自动化脚本的。
    # options.add_argument(r"--user-data-dir=C:\Users\15414\AppData\Local\Google\Chrome\User Data")

    # options中的一些常用参数设置如下：

    # 启动隐身模式
    # options.add_argument('incognito')
    # 去除控制台多余的信息：避免掉无用的信息内容
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #控制浏览器日志输出级别，3 表示只输出警告以上（减少控制台噪声）
    options.add_argument('--log_level=3')  # 设置 Chrome 浏览器的日志级别
    '''
        --log_level=3 日志级别
        在生产环境中，一般建议将日志级别设置为较低的级别（如 3）以减少日志量。而在开发和调试过程中，你可能需要更详细的日志信息，可以将日志级别设置得更高（如 1）
        0：DEFAULT，使用默认日志记录级别。
        1：VERBOSE，输出详细的日志信息，包括调试信息。
        2：INFO，输出一般的信息级别日志。
        3：WARNING，输出警告级别的日志。
        4：ERROR，输出错误级别的日志。
        5：FATAL，输出严重错误级别的日志。
    '''

    # 在某些环境下禁用 GPU 加速（稳定性更好）。
    options.add_argument('--disable-gpu')  # 禁用 GPU 加速

    # 当网站证书无效时，继续访问不报错。
    options.add_argument(
        '--ignore-certificate-errors')  # 它用于忽略证书错误，当 Chrome 浏览器访问一个使用无效或过期的 SSL 证书的网站时，会弹出一个警告页面，提示用户连接不安全。通过添加 --ignore-certificate-errors 这个选项，可以告诉 Chrome 浏览器忽略这些证书错误，继续加载页面而不显示警告。

    # 关闭 Chrome 的沙盒模式（某些环境下必要）。
    options.add_argument("--no-sandbox")  # 禁用沙盒模式

    # 关闭所有浏览器扩展插件（避免干扰）。
    options.add_argument("--disable-extensions")  # 禁用扩展

    # options.add_argument("--headless")  # 使用无头模式运行浏览器
    # options.add_argument("--window-size=1920,1080")  # 自定义窗口大小
    # options.add_argument("--blink-settings=imagesEnabled=false")  # 禁用图片加载
    # options.add_argument("--user-agent=Your User Agent String")  # 使用用户代理

    # 将浏览器语言设置为英文（美区）。
    options.add_argument("--lang=en-US")  # 设置为英文（美国）


    # 禁用浏览器自动化控制警告提示
    # 防止「Chrome 正在被自动化软件控制」提示，避免某些检测机制。
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 返回options对象
    return options
