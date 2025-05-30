import pytest
from config.conf import ConfigManager
import time
import csv
import threading
from page.wms_pages.form_generate.form_gen import WmsElements

"""
fixture + 生成器yield   一起实现了前置启动，后置清理的装饰器
@pytest.mark.parametrize 会在 @pytest.fixture 之前执行

ddt数据驱动**

​    **pytest解析****@pytest.mark.parametrize****时 -ddt数据驱动** 

​    **自动生成 使用****不同参数****的****测试用例** **让测试函数以不同的参数运行多次**

​    **写个 read_csv_file()函数**

​      **先****csv.DictReader****(file)** **逐行****读取 CSV 文件 转换成****字典**

​      **使用生成器*****yield\*** **控制数据****逐行读取** **一个一个来 减少内存占用，并一次性生成所有测试用例**
"""
@pytest.fixture(scope='function', autouse=True)
def open_baidu(drivers):
    drivers.get(ConfigManager.WMS_URL)
    yield
    # print("后置")

# read_csv_file提供数据
def read_csv_file(file_path):
    """生成器方式去读取csv里面的数据来做数据驱动测试，
    yield关键字来控制一行一行的读取字典里面的内容（
    字典里面的数据是隐形的，还未产生，就和奶糖盒子一样的道理）"""

    """✅ 生成器 yield 只是在 read_csv_file() 内部用于控制数据逐行读取，
    但 pytest.mark.parametrize 在解析时会立即将所有 yield 生成的数据取出来。
"""
    with open(file_path, 'r', newline='') as file:
        # csv.DictReader(file) 逐行读取 CSV 文件，并转换成字典
        reader = csv.DictReader(file)  # 这是一个迭代器对象，把每次读取出来的数据都放到字典里面存起来，下面用一个for循环一次一次的去读取字典里面的数据，确保不会一次性将所有的数据读取到内存中。
        for row in reader:  # 如过下面没有生成器，那么这里直接全部数据都遍历一遍，如果有生成器就会卡住，一个一个来，接收到next方法才会读取下一行。
            yield row['username'], row['password']

"""
@pytest.mark.parametrize('username, password', read_csv_file(r'data/data.csv'))
让 pytest 自动调用 read_csv_file()。
相当于
@pytest.mark.parametrize('username, password', [
    ('admin', '123456'),
    ('user1', 'password1'),
    ('user2', 'password2')
])
测试执行时，pytest 只会运行 test_login()，不会再调用 read_csv_file() 读取新数据
"""
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
