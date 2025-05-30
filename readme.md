# 一言蔽之

==亮点：0-1搭建框架➕钉钉集成==

定位 断言 —— 封装框架和工具类 —— 高级语法 优化框架结构 —— 用源码逻辑 优化框架运算时间,代码结构,执行效率,内存管理,垃圾回收

**命令行输入pytest后：**

**UI：**

- [ ] 第一阶段 解析pytest.ini文件：配置默认参数 指定测试用例的位置 					实现多线程 生成测试报告 选择性执行用例 失败重跑操作

  ```
  	1. pytest-xdist插件自动把测试用例分给多个线程并发执行
  
  ​		每个线程 都可以==独立==打开一个网页运行测试用例
  
  ​		一般使用10~20个线程为最 佳
  
     	2. ==一个cpu== 同一时刻 只能执行一个线程，只是调度每一个线程的速度非常快 看起来是并发的而已，CPU不断调度实现==宏观并发 但微观并行==
  
  ​	3. ==多个cpu== 才能真正意义上实现多个测试用 例并发执行
  
  pytest -n 2
  pytest -n auto
  	;自动检测可用的CPU核心数量 使用对应数量的进程并行运行测试 充分利用计算资源
  pytest -n 4 --dist=loadfile
  	;使用4个进程并行运行测试，并使用"loadfile"分发插件进行测试运行
  ```

- [ ] 第二阶段 收集测试用例 这时候加载测试类 

  在测试登陆账户密码的场景中 通过pytest.mark.paramatrize生成所有的测试用例

  @pytest.mark.parametrize('username, password', read_csv_file(r'data/data.csv'))修饰测试用例 ，pytest收集测试用例的时候会自动执行 根据里面的数据生成所有的测试用例 

  

  读取csv的函数是用csv.DictReader创建迭代器 for循环遍历迭代器 然后用yield控制一行行读取csv里面的数据

  ```apl
  1、实现_iter_方法 和 _next_方法的对象叫选代器对象也就选代器；
  2、只实现_iter_方法的对象叫可选代对象，列表，字典，元组，集合等都是可迭代对象
  3、range以及python的四大数据结构都是可选代对象，
  要先用iter函数变成选代器对象 再用next方法遍历其中的每一个数据，
  也可以直接用for循环来遍历可选代对象的数据，for循环里面自动调用iter再调用next方法。
  
  ddt数据驱动测试在框架中的使用
  1、Data-Driven Testing：数据驱动测试
  2、利用迭代器和生成器来一行一行的读取，而不是一次性全部读取到内存中，这样的好处是自动化框架执行的时候效率比较高，并且不太暂用内存，如果不适用生成器的方式，就会导致一次性读取所有csvV中的数据加载到内存中，可能会导致崩溃。
  3、使用@pytest.mark.parametrize（参数一，参数二，list）来做pytest的数据驱动。List中有多少个数据，就会执行多少遍测试用例
  
  迭代器就是用来遍历可迭代对象
  
  生成器是一种特殊的迭代器，通过yield关键字来创建，生成器运行时每次遇到yield时，函数会暂停并保存当前运行信息，下次执行next时从暂停位置继续运行
  ```

- [ ] 第三阶段 解析fixture装饰器 执行前置操作 按scope顺序session model class function

  在conftest用fixture和生成器 实现全局管理driver函数							   

  创建浏览器实例driver=webdriver.chrome，然后写yield driver					

  这样其他函数写了drivers作为参数 就获得yield driver返回的driver实例，然后driver.quit关闭

  在测试类里面用fixture和生成器实现执行测试用例前登陆 执行测试用例后登出的操作

  

  测试类里面用装饰器和生成器实现自动登陆登出的功能(yield前后 创建页面实例 对页面元素操作)

  装饰器修饰的函数把dirvers作为参数 自动获得driver实例

  打开浏览器drivers.get(url) 然后创建页面的实例 对页面进行登陆操作

  yield下面通过实例进行登出的操作

  ```apl
  装饰器是修饰函数的函数 增加功能但不改变原函数代码
  参数是一个函数，内部还有一个函数，返回值是一个类似原函数的函数对象
  
  调用被修饰的函数 本质是执行装饰器函数
  装饰器会把被修饰函数作为参数 传入装饰器的内部 然后执行装饰内部的函数
  
  fixture 提供测试函数要使用的资源 管理执行时机 在合适的时机提供数据或资源
  scope：指定 fixture 函数作用域范围
  		session全局共享 运行一次执行一次
  		model每个文件执行一次
  		class每个类执行一次
  		function每个函数用例执行一次(默认)
  autouse：指定 fixture 是否自动运行，需不需要在测试函数中显式引用
  @pytest.mark.xx
  @pytest.mark.parametrize()
  @property 就是让函数变成一个属性，调用的时候不用写()
  
  有yield关键字的函数就是生成器 调用next方法的时候才会执行yield后面的
  pytest调用 next() 方法执行到 yield 语句，测试函数执行完成后，再次调用生成器的 next() 方法，执行 yield 之后的清理代码
  
  2、装饰器的调用顺序？ 小北如果调用函数 say_hello，该函数就会调用装饰器函数，装饰器函数将会把say_hello 函数作为装饰器函数的参数传入装饰器的内部，并且执行装饰内部的函数。 3、如何将装饰器融合到pytest框架里面? 3.1、全局管理driver，运行测试用例的时候先调用driver传入测试用例中，测试用 例就可以使用driver来操作浏览器了。 3.2、实现执行测试用例之前先登录或者先打开网址，执行测试用例之后再自动登 出的操作。 批业跳 1、如果是装饰器，就有传参（是一个函数） 2、有返回，返回了一个对象函数（只是这个函数没有任何改装，就是原参数） 于装饰器还有很多，大家可以自已看看文档学习更多的知识，不过掌握到这里已经足够了。 3、@property的使用，就是让函数变成一个属性，调用的时候不用写0，仅此而已。
  
  1、scope：装饰器作用域范围 2、params：可以传参数 3、autouse：是否自动调用，比如可以用来自动登录和自动登出，而不需要手动调用登录 登出函数。 4、ids：一般和params 结合起来使用，标记每一个参数对，方便追溯是哪一个参数对对 应的测试用例执行失败了。
  
  什么叫生成器？ 1、只要是实现了yield关键字的函数都是一个生成器 2、生成器的特点是，当调用者执行到yield就会卡住，然后把yield后面的参数返回给 调用者 3、当接受到nextO函数的命令时才会执行yield关键字下面的代码 怎么把生成器融入到我们pytest框架中? 1、自动登录登出中要使用生成器 实现了执行测试用例之前先执行前置操作【登录】【因为有装饰器】直到代码运行 到有yield关键字的时候才会卡住，当执行完测试用例之后，pytest自动调用next函数， 才会去执行yield关键字后的后置操作【登出】。 【执行for循环的时候也会自动调用next函数】
  
  
  全局管理driver：
  1、这里的fixture是用来让其他测试用例test来调用的，只 要调用了drivers函数，就可以使用函数内部的driver实例 就可以打开浏览器了，autouse是自动执行的意思，不管你 掉不掉用他，只要在pytest中的测试用例都会自动化调用 drivers函数 2、里面有一个yield关键字，大家记住只要是一个函数内部 有yield关键字，那么这个函数就是一个生成器，当函数执行 到yield关键字的时候就会卡在这里，不会继续执行下面的命 令，如果调用者没有发出next(的命令，他是不敢往下执行 的，这里我们在pytest中，默认只要执行完一个测试用例 就会马上调用一遍nextO函数，所以当用例执行完，才会执 行driver.quitO函数，这就实现了生成的使命了，用例执行 前生成driver，用例执行后关闭脚本，完美！
  ```

  

- [ ] 第四阶段 执行测试用例

  通过描述符(实现get set delete中任意一个方法的类) 封装元素定位和操作 - 在basepage.py

  实现传入键值对就能定位到元素 对元素赋值就能在输入框中输入字符串 

  basepage.py为基础封装(字典+3个类)，login_page.py为具体页面对象

  在page里写元素的定位和操作 然后在测试用例里创建page实例 就能对页面进行操作了

  测试用例中调用 login_page 的属性和方法就可以 

  不用每次都写 find_element 和 send_keys 可以在多个页面类中重复使用相同的元素定位方式

  ```apl
  # 先用id定位，如果没有id，考虑xpath或css_selector，因为浏览器可以直接导出表达式
  把描述服定义为类属性 用该类的实例访问属性 python自动调用对应方法实现 属性访问控制
  # 初始化描述符
  input_account = PageElement(xpath='...')
  1、触发 PageElement.__init__ 接收键值对
  	_LOCATOR_MAP字典 根据关键字'xpath'查找_LOCATOR_MAP['xpath'] 得到By.XPATH
  	(id='kw')变成（By.id, 'kw'）	
  	字典把键转化成selenium需要的by类型
  	实现分解传入的键值对 让findelement可以直接当作参数使用
  
  # 实例化页面对象
  page = WmsElements(drivers)
  2、触发 父类PageObject.__init__ 保存driver 后面使用
  	
  # 访问属性时自动调用 __get__里的find_Element 
  page.input_account
  3、访问自动触发 pageElement 的 __get__方法里的find_Element 
  用保存的定位信息定位到对应的元素（找不到等待5秒）并返回找到的元素
  相当于driver.find_element(By.XPATH, "...")
  get实现元素定位find_Element方法
  	
  # 赋值时自动调用 __set__
  page.input_account = 'abc'
  4、赋值自动触发 PageElement 的 __set__方法
  set方法先调用 __get__ 找到元素 然后执行send_keys('abc') 在输入框中输入文本
  相当于element.send_keys("admin")
  set实现sendkeys方法
  
  1、只要实现了_get_，_set_，_delete_中的任意一个方法的类就是一个描述符 2、_get_方法是在描述符被调用的时候就会被首先触发（用作元素定位) form_gen.username这个就是get 4、_set_方法是在描述符对象被赋值的时候被触发执行（用作元素send_keysO的封装） form_gen.username="admin"就是 set 4、_delete_方法，我目前实在是找不到怎么利用起来，所以如果被问到，直接说自动 化框架中暂时用不到。
  ```

用js脚本实现滚动条

在common目录封装工具类

用pil模块进行截图然后抠图出验证码的地方 用dddocr进行识别

用pywinauto的desktop类定义文件框的文件然后用inspect工具

```apl
UI自动化中验证码识别

				简单验证码：Pil模块截图 ddddocr模块做图片识别；先整个页面截图 确定验证码坐标 image.open打开整个页面的截图 crop方法抠出来 用ddddocr的classification方法识别验证码；复杂验证码要用付费的第三方api识别 直接让开发换成固定验证码

UI自动化中文件上传

				用pywinauto模块的desktop类定位文件框 然后用inspect工具定位 input框输入文件位置 点击打开
```



```apl
UI自动化中图片识别
				用pil模块的Image.open
```



```apl
UI自动化中颜色识别
用pil模块进行截图 然后用opencv进行颜色识别
具体是用hsv定义各种颜色的范围 然后存入字典 用opencv的函数识别图片的最大颜色 然后进行判断；传入两个元素 根据他们的坐标写个逻辑判断

				传入 -driver 元素 屏蔽的颜色

				我主要是通过 opencv 和 pil 库来实现这个功能的,通过 Pil 模块截图，截取到需要识别的组件的图片，

			再通过 opencv 去识别组件的颜色，能够基本上准确识别出来。

				内部逻辑是，先定义颜色的取值范围，这里用的是 hsv 颜色空间，h,s,v 三个通道都有一个取值范围，

				这样就能规定某一个颜色的取值范围了，(如果问到黑色的取值范围是多少,可以说是查的百度)

				并将多种颜色存入一个 dict 字典中,方便后续匹配,

				之后用 opencv提供的函数方法找到组件中颜色面积最大的颜色，并返回结果，最后去做断言即可。

				中间还提供了可以屏蔽的颜色参数选项，比如一个组件有红蓝，两种颜色，我去识别的话，不能同时输出两个颜色，

				可以先屏蔽红色去识别蓝色并断言，再屏蔽蓝色去识别红色并断言。
```



```apl
UI自动化中组件是否重合

				我写了一个工具类来判断两个组件是否重合，传入两个组件，如果没有重叠的地方就返回 false，如果有重合的地方就返回 ture。然后对返回的值做断言。

				工具类的内部逻辑是先获取到传入的两个组件的左上角坐标，以及组件的宽和高，再去写一个逻辑判断是否有重合的可能性，假设会重合，那么必定有一个组件的x坐标会小于另一个组件的x坐标加上宽度，y坐标也是同理的，只要满足这几个条件中的任意个，就能判断他重合
```

- [ ] 第五阶段 pytest 通过 fixture 机制 测试用例执行完后自动调用next函数 然后执行yield后面的后置操作 反着scpoe顺序

- [ ] 底层原理：Python代码通过webdriver发送操作指令到浏览器 、浏览器驱动程序把代码转化成浏览器能识别的内容 、操作完后浏览器把结果返回给webdriver接口 再返回给python脚本进行断言


## 自动化开展

当时项目开发迭代了3个月了，总用例数突破1000+，需要回归的测试用例也有近300条

手工回归测试的效率太低,并且项目旧接口比较稳定 适合做接口自动化，页面功能比较稳定 适合做UI自动化

所以用自动化测试框架来提高回归效率

我从0到1搭建了基于KDT的接口自动化框架和基于PO模式的UI自动化框架 并且结合GitHub和Jenkins实现CI流程

- 用python做接口测试和懂一点计算机网络，那么我会找一个我们项目中用的第三方软件的文档，把它的接口鉴权这几行文档抄到题目里。然后让来面试的人讲下用python怎么实现这个接口调用
- 各种鉴权的用法，区别。比如 cookie session 鉴权跟token 鉴权有啥区别，为啥用这种不用那种。但知道放header 其实也够了。
- 实际上我项目里header我都处理好了，我估计一年也不需要他写一次header

## 框架搭建

### UI

技术栈：

python+selenium+pymysql+pytest+allure、采用PO模式分四层,对象层封装对页面元素的定位方法,操作层封装对元素的操作,业务层封装业务操作顺序,数据层封装测试数据

目录结构：

pages页面元素；testcases测试脚本；report测试报告；data测试数据ddt数据驱动；common封装各种工具类；

screenshot保存截图；config常量；log存放日志；两个核心文件conftest和pytest.ini 和 安装第三方库的文件requirements.txt 




**元素定位不到的情况有哪些？**	

​	1、文件上传 -第三方库pywinauto定位window系统框 2、悬浮元素 -用debugger固定在页面上再定位 3、动态id -用xpath 4、句柄跳转 -用switch to定位

**高亮元素怎么定位**	

​	(Css的一些背景样式) 用css样式的class选择器定位

**一个元素怎么都定位不到**	

​	pyautogui绝对定位





**UI自动化怎么写？**	

​	1、功能测试用例一步步转化成代码 2、预期结果转化成断言 3、写完提交到git和Jenkins持续集成ci 回归阶段跑一下看有没有bug







**pytest？**

​	Pytest有夹具fixture可以结合装饰器 生成器实现前置处理 后置清除 —————————@pytest.mark.skip()、@pytest.mark.skipif()、@pytest -k “dog”



**PO模式？**	1、PO模式就是把元素和操作分开 2、把页面的结构和功能封装到一个对象里 3、测试用例代码通过操作这些对象和页面交互 而不是直接操作页面的元素



对象库层:封装定位元素的方法O

操作层:封装对元素的操作O

业务层:将一个或多个操作组合起来完成一个业务功能。比如登录:需要输入帐号、密码、点击登录三个操作0



**元素定位不到的情况有哪些？**	

​	1、文件上传 -第三方库pywinauto定位window系统框 2、悬浮元素 -用debugger固定在页面上再定位 3、动态id -用xpath 4、句柄跳转 -用switch to定位



**高亮元素怎么定位**	

​	(Css的一些背景样式) 用css样式的class选择器定位



**一个元素怎么都定位不到**	

​	pyautogui绝对定位



**数据驱动ddt**	

​	把数据放到csv文件 然后写个函数用生成器迭代器一行行读



**失败用例重跑**	

​	pytest.ini文件加上--reruns=2



**让自动化用例跑的更快**	

​	多线程 -pytest-xdist插件 pytest.ini文件用参数-n指定线程数 -一般20线程跑2 3小时



**装饰器**	

​	1、参数是函数 内部还有个函数 返回值是一个函数对象 2、@装饰器函数

修饰函数的函数,不改变原有函数代码的基础上,动态的改变函数的功能

在我的框架中,用装饰器生成器实现全局管理drvier 自动登陆登出



**fixture**	

​	 1、Fixture源码传参有一个是函数 内部还有函数 返回值也是函数对象 2、自动登陆 登出 3、自动传入driver 清理driver 全局管理diver



**自动化bug**	

​	一个表单的电话号码字段 自动化断言失败 看了截图发现框没有数字后面写的11/11 而不是0/11 -清空数字的时候没有动态改变状态



**可迭代对象,迭代器,生成器?**

​	可迭代对象一般是能直接用于 for 循环遍历的数据对象,

​		比如:常见容器类型数据str, list, tuple, set, dict等都是可迭代对象,还有一些函数的返回值如 range() 函数的返回值也是一个迭代的对象

​	迭代器和可迭代对象很像,是可以被 next() 函数调用并不断返回下一个值的对象,但区别是可迭代对象一次性生成全部值,但迭代器每次被 next() 函数调用只生成一个值,不会一次性全部生成

​	生成器是一种特殊的迭代器，	函数有yield的都可以叫生成器 被调用的时候执行到yield就会停止 接收到next函数后才会执行后面的





什么是可迭代对象,迭代器,生成器?

可迭代对象一般是能直接用于 for 循环遍历的数据对象,比如:常见容器类型数据str, list, tuple, set, dict等都是可迭代对象,还有一些函数的返回值如 range() 函数的返回值也是一个迭代的对象迭代器和可迭代对象很像,是可以被 next() 函数调用并不断返回下一个值的对象,但区别是可迭代对象一次性生成全部值,但迭代器每次被 next() 函数调用只生成一个值,不会一次性全部生成生成器是一种特殊的迭代器，通过 vield 关键字来创建,生成器运行时每次遇到 vield时,函数会暂停并保存当前运行信息，下次执行 next() 时从暂停位置继续运行





**验证码**

​	对于线上环境

​		如果是图片验证码,我会优先考虑ocr去识别图片上的字符,其实识别率不高,还不到50%

​			 1、简单验证码识别：

​			Pil模块截图 ddddocr模块做图片识别

​			把整个登录页面截图 确定验证码图片坐标 抠图 用ddddocr的classification方法识别验证码写到input框

​			2、复杂验证码：

​			调用付费第三方api的AI识别 

​			showapirequest/ddddocr模块处理有横线的验证码

​		如果是短信验证码，我会到验证码的存储位置去读，比如数据库读取

​	对于测试环境

​		可以让开发直接关闭验证码或者设置万能验证码

​		也可以将部分账号添加到白名单来跳过验证





**Jenkins每天都跑吗？**	

​	用jenkins定时晚上下班后跑一跑 隔天早上看看测试报告有没有异常



**描述符(类) 元素定位重新封装**	

​	1、实现 get set delete任意一个方法的类  

​	2、在get里写find_element然后传入一个键值对就能实现元素定位

​	3、在set里写的sendkeys 然后元素赋值的时候就会触发 set里的sendkeys实现赋值



**怎么选择执行测试用例**	

​	1、标记@pytest.mark. x然后用pytest -m x参数指定要运行的函数 2、指定包含表达式的函数pytest -k “” 3、指定目录 pytest test/



**全局管理driver**	

​	在conftest配置一个dirver函数 使用fixture的session参数 然后哪里需要用到driver的时候直接参入dirver就可以了



**有哪些断言**	

​	文本匹配断言 元素状态断言 元素存在断言 页面跳转断言 、难的场景：文件上传图片 图片是不是我所上传的 图片颜色识别



**元素定位xpath和css**	

​	Xpath功能强大 性能稍差



***selenium\*****中有哪些元素定位方式*****?\*****你如何决定使用哪种定位方式*****?\***

​	属性动态变化的元素怎么定位

​		先找出变化规律，在元素定位时，用规律去生成对应的要定位的属性即可

​	高亮的元素怎么定位

​		元素高亮一般css样式设置的,可以根据css选择器进行定位隐藏的元素怎么定位

​	隐藏元素的定位方式和可见元素是一样的，只不过可能无法对其进行交互操作

​		可以使用js脚本来绕过这些限制

​	定位不到元素会有哪些情况

​		可能是动态元素,属性不固定

​		可能元素被遮挡,需要最太化窗口或滚动页面才可见 

​		可能元素在iframe中,需要切换iframe

​	页面元素没办法提取怎么办

​		可以用pyautoGUl做图像识别

有id, name, class_name, tag_ name, link text, partial link text, xpath,css selector等八种定位方式

我一般会先考虑id定位,

如果元素没有id,再考虑xpath或css selector,因为浏览器可以直接导出表达式



**显示等待和隐式等待是什么意思，和sleep函数有什么区别?**

​	元素等待是为了确保页面元素加载完成的手段隐式等待是设置一个全局的等待时间,如果定位元素超时会报NoSuchElementException异常0显式等待可以为定位不同元素设置不同的超时时间,更加灵活,定位超时会报TimeoutException异常0time.sleep(3)是强制等待,直接暂停线程,用法比较暴力



**你们UI自动化的用例数,覆盖率，通过率数据是多少?**

​	上个项目我跟了一年,总用例数大概3000条左右,其中大概有1000条左右是需要自动化回归的测试用例我们做UI自动化的覆盖率目标是30%,基本都完成了

还有一部分接口没有覆盖的原因是:某些功能的使用率较低,部分功能涉及支付和第三方服务,还有一些涉及0硬件操作的用例,比如扫码入库,这些我都是手工完成回归的通过率基本都是100%,毕竟都是旧功能了











## Python

我用python写了个工具，可以生成对应格式和大小的文件 	我们公司文件上传的功能较多,我就写了一个工具,

​	可以生成对应格式和大小的文件

可变数据类型：列表list 集合set 字典dict ；改变对象内部的值 内存地址不变

不可变数据类型：int float 布尔 字符串str 元组tuple ；创建后对象里的值不能改变，修改是创建新的对象 内存地址会变 

列表[]存储动态变化的数据 可以增删改查

元组()储存不变的数据 只能查询，元组是只读的列表 元组的性能优于列表

列表去重：

使用集合的特性

先用set函数把列表转换为集合 再用list函数把类型转换回列表

循环遍历方法去重

先定义一个空列表 然后循环遍历原列表元素 如果元素不在空列表 用append方法把元素添加进去



字符串反转：

切片的方式 设置步长为-1即可

内置函数的方法思路是先使用reversed函数反转，再使用join函数进行拼接

浅拷贝 深拷贝：

本质，在于 Python 的变量赋值默认是引用传递。浅拷贝只复制第一层结构的引用，而深拷贝会递归复制所有层级的数据对象，从而避免多个变量共享同一数据时产生的联动问题变量赋值让多个变量引用同一块数据

都用copy模块实现 浅拷贝copy函数 深拷贝deepcopy函数

对于不可变类型的数据 浅拷贝和深拷贝都 没有新建外内层对象 就复制数据的引用 不会开辟新的内存地址

对于可变类型的数据

浅拷贝 只新建外层对象 外层开辟新的内存地址 复制数据的值，内层的数据只复制引用 内层对象共享

深拷贝 新建外内层对象 内外层都开辟新的内存地址 把值复制过来

冒泡：

核心是两层嵌套循环来实现

外层控制循环的轮次，每一轮找出当前最符合的元素，并冒泡

内层控制每个元素两两比较的次数，以及元素位置的交换



**说下python中的推导式?**

​	用于从一个可迭代对象中创建新的容器

​	比如 [x**2 for x in range(1,11)]用于创建一个包含1到10的平方的列表



python中如何跳出循环?

​	break,用于结束循环

​	continue,用于跳出本次循环,直接进入下一次循环



列表中的数据如何拼接成字符串?

​	可以先定义空串，在通过for循环和+运算符来拼接列表中的数据

​	可以用字符串的join()方法,列表作为参数传进去就得到拼接后的字符串了



如何通过切片获取一个数据中倒数的3个元素?

​	首先很多数据类型都支持切片的操作,比如字符串,列表,元组等

​	切片的语法是储存数据的变量名后面跟个中括号,中括号内分别是起始位,结束位 和 步长

​	那么想获取倒数的三个元素只需要设置起始位为负3即可(形式如:变量名[-3:]



字典怎么遍历?

​	变量名.keys() 获取键列表

​	变量名.values() 获取值列表

​	变量名.items()获取包含了键和值的元组的列表



如何合并两个列表或字典?

​	合并列表可以用+运算符或list1.extend(list2)的方法

​	合并两个字典使用{**dict1，**dict2}或dict1.update(dict2)方法



如何捕获一个异常?

​	可以使用 try….except . 语法来捕捉异常,

​	如果后续有需要执行的代码可以放在 finally 代码块中



python函数传参时的*和**是什么意思?

​	*用于接收不确定个数的参数,并打包成一个元组,定义形参时通常用*args *用于处理元组/列表等数据

​	**用于处理字典数据









## Docker

```dockerfile
# mysql
docker volume create mysql_data

docker run --name car-mysql \
    -v mysql_data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=123456 \
    -e MYSQL_DATABASE=car \
    -e MYSQL_USER=test \
    -e MYSQL_PASSWORD=test-pass \
    -p 3306:3306 \
    -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

```dockerfile
# redis.conf
port 6379
bind 0.0.0.0
protected-mode no
dir /data
dbfilename dump.rdb
save 900 1
save 300 10
save 60 10000
appendonly no

docker volume create redis-data

docker run --name car_redis \
	-v $(pwd)/redis.conf:/etc/redis/redis.conf \
	-v redis-data:/data \
	-p 6379:6379 \
	-d redis redis-server /etc/redis/redis.conf
```

```dockerfile
# rabbitmq
docker volume create rabbitmq-data

docker run -d \
    --name rabbitmq \
    -p 5672:5672 \
    -p 15672:15672 \
    -v rabbitmq_data:/var/lib/rabbitmq \
    -e RABBITMQ_DEFAULT_USER=admin \
    -e RABBITMQ_DEFAULT_PASS=123456 \
    rabbitmq:management
```

```dockerfile
# vue-nginx
docker build -t nginx-vue .

docker save -o nginx-vue.tar nginx-vue

sudo docker load -i /root/nginx-vue.tar 
docker run -d -p 80:80 --privileged=true nginx-vue
```

```dockerfile
# _back
docker build -t car_back .

docker save -o car_back.tar car_back

sudo docker load -i /root/car_back.tar
docker run -d --name car_back -p 8000:8000 car_back
```

```
# 进入容器
docker exec -it ID bash
```

```
# volume
docker volume ls

docker volume inspect rabbitmq-data
```

```
# 权限问题
docker exec -it competent_mendeleev chmod 644 /usr/share/nginx/html/index.html

docker exec -it competent_mendeleev find /usr/share/nginx/html/ -type f ! -perm -o=r -ls

docker exec -it competent_mendeleev find /usr/share/nginx/html/ -type f ! -perm -o=r -exec chmod 644 {} \;
docker exec -it competent_mendeleev find /usr/share/nginx/html/ -type f ! -perm -o=r -ls
```

```
# 手动加载插件
# 进入mysql
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;
```



## Jenkins

下载钉钉插件 系统管理里新增机器人 任务里添加机器人

<img src="/Users/chu/Library/Application Support/typora-user-images/image-20250526212540794.png" alt="image-20250526212540794" style="zoom:30%;" />

<img src="/Users/chu/Library/Application Support/typora-user-images/image-20250526212738553.png" alt="image-20250526212738553" style="zoom:25%;" />

下载GitHub git插件，系统管理添加凭据，系统配置里添加GitHub服务器、配置git、配置定时构建、执行shell

全局工具配置git 配置allure



实现自动化代码CI流程：

​	代码传到GitHub仓库 GitHub仓库设置webhook 在Jenkins上配置GitHub服务器

​	在jenkins的任务里写shell脚本，配置钉钉机器人

​	生成allure报告 触发器选择github hook

​	实现webhook触发 GitHub仓库更新代码Jenkins就自动构建 和 定时构建 并且生成allure报告 通知钉钉

​		其中jenkins监听触发条件然后执行任务

​		定时构建就是Jenkins主动从GitHub拉取 在Jenkins配置git地址 任务里源码管理填写GitHub仓库地址和账户密码 设置定时构建

​		webhook触发 先在GitHub项目里配置webhook 填写Jenkins地址和secret 然后把secret添加到jenkins凭据 配置GitHub服务器信息 任务里面配置secret 构建触发器选择 GitHub hook 步骤里写个shell执行pytest命令

   			*GitHub*发送*webhook*请求的时候通过*paylod*和*secret*使用*HMAC-SHA256*计算签名
   	
   			*jenkins*自动使用*GitHub*发送来的*payload*和本地存储的*secret*用同样的方法*HMAC-SHA256*计算签名
   	
   			*jenkins*自动把两个签名进行对比

 下载allure插件 配置allure的地址 任务里构建后操作 配置json的文件路径

 下载钉钉插件 钉钉群添加自定义机器人secret 然后在Jenkins配置钉钉 填写webhook地址和secret 并在任务里添加



DevOps是一种把开发和运维紧密结合文化 

GitOps是DevOps文化的实现方式 由iac+git+cicd流水线组成 

​	iac是用代码管理 自动化配置

​	cicd流水线分为pull push模式

​		push模式是Jenkins主动拉取GitHub的代码 构建打包 把生成的产物推送到服务器 运行实例 实现项目部署上线

​		pull模式是把代码打包生成docker镜像 上传到镜像仓库 服务器(tomato)主动从镜像仓库 pull把镜像拉过来 运行前后端docker实例 通过k8s部署上线 中间argo cd监控他们的状态 实现项目部署上线

​			argo cd就是去管理k8s集群 可以去创建项目 ，这个项目只要他的状态和git仓库状态不一致的时候说明git仓库有代码变化 会主动去同步一下中间间实现cd全过程 自动构建自动部署 最终可以用url访问改动过的网站













Jenkins拉取前后端代码 —— docker部署（前端：nginx.conf配置地址转发，创建dockerfile把打包好的dist放到nginx里 暴露端口 运行）



git push - Jenkins构建 - docker镜像打包 - 推送仓库 - 部署运行

CI持续集成 自动化

CD通过docker项目前后端代码部署上线



docker的使用：

docker容器技术 把应用打包成镜像(前后端) 运行成容器(测试环境 上线) ；容器和容器之间相互隔离 互相通信

运维写好环境部署脚本 然后我使用jenkins的一键部署功能

​	制作本地镜像仓库

​	使用docker build基于dockerfile分别制作 前后端镜像 并通过docker push上传到本地仓库备份

​	通过docker run运行前后端镜像,生成对应的实例

​	然后就可以访问了

​	（合理分配 最大化利用服务器资源；环境部署能做到各个测试/预生产环境一致；一致性 隔离性 易于管理）

我工作中没有用到 docker，已经有一套完整的 cd 流水线了，不过我看过相关的学习资料和公司的搭建文档，我知道怎么用的



Jenkins的使用：

实现CI CD,租阿里云的服务器,运行Jenkins服务

CI持续集成

检测前后端git仓库代码变动 代码更新则触发自动部署测试环境

再通过git拉取最新的自动化测试代码,执行并生成alure测试报告,生成的测试报告发送到钉钉群

只有在dev分支上经过了自动化测试的代码 才会被提交到test以便进一步完成系统测试

CD持续部署

在验收测试通过之后,Jenkins会通过git把代码合并到主干

然后拉取主干最新代码进行构建,把代码转化为可执行docker镜像

然后执行运维配置好的部署脚本

​	docker镜像,通过push上传镜像到镜像仓库,再把镜像运行为实例，同时用到了k8s进行集群部署

jenkins也会用于线上巡检,定时每天凌晨3点运行一次自动化测试



​	docker compose：**声明式配置文件**描述整个应用 -使用一条命令完成部署

​	部署compose应用 默认读取docker-compose.yml/.yaml



最关键的有哪些指令:

docker pull :拉取镜像到本地

docker images :列出所有的镜像

docker ps :列出当前系统中正在运行的容器

docker commit :生成镜像

docker build :基于 dockerfile 生成镜像

docker exec-it jenkins bash :进入容器内部

docker run -it :把镜像运行成为实例对象

docker rm -f:删除镜像 docker rmi

exit:退出容器内部环境

docker logs+容器名称:查某个容器的 docker 日志



利用 docker 从0到1发布上线的整个过程：

1、我们要制作本地镜像仓库

2、利用 docker build 的方式基于 docker file 去制作含有网站代码以及各种依赖的前后端 docker 镜像，并利用 docker push 上传到本地仓库中【备份)

3、再利用 docker run 运行前后端镜像，并生成前后端实例

就说明部署成功

4、用户通过网址访问网站，并且接口也有正常响应数据的情况，



怎么在这个容器内去执行一些命令：

进入容器内部，这进去之后就可以执行其他命令了docker exec - it jenkins bash可以换成其他的。这里的jenkins 是容器的名称 可以换成别的



docker 怎么去拉一个镜像，怎么把它部署起来：

先 docker pull 镜像，然后再运行 docker run 镜像，最后生成 docker 的实例，就能部署起来了



怎么去 docker 里面去终止掉某个进程：

(先进去，再 kill)

docker exec -it jenkins /bin/bash

kill pid







-- docker里面运行mysql

docker run -d --name mysql_container \

 -e MYSQL_ROOT_PASSWORD=123456 \

 -e MYSQL_DATABASE=testdb \

 -p 3306:3306 \

 -v ~/docker/mysql/data:/var/lib/mysql \

 mysql:latest



-- docker里面运行Linux

docker run -d -it --name mywebserver -p 8080:80 ubuntu:latest

-- 进入Linux

docker exec -it linux_car bash



你在使用 docker 的过程中，常用的哪些命令：

Systemctl restart docker

docker stop 容器ID:停止运行的容器

docker push

docker built

docker run -it :重建，会丢容器内部的配置数据

docker start+lD 这一条命名和上一条命令有区别，不会丢失容器内部的配置数据容器 

docker restart +容器ID :重启容器

docker images

docker tag

docker cp 本地文件想上传到容器里面，怎么上传?说出命令?

Docker pull redis: ...tag

docker ps -a:列出当前系统中所有的容器(包括运行的或是已停止的)-all

docker ps :列出系统中正在运行的容器,不包括已经关闭的容器

Docker commit docker build 构建新镜像

Dockerfile:不是一个指令，是一个基于 docker build 的打包必须文件。Exit 退出

docker exec -it jenkins /bin/bash进入到正在运行的 docker 中，首先用 docker ps 看看名字

docker cp /root/gitUl_auto/automation/ df8b61fd9fcb:/var/ienkins home/workspace

这一串代码是将容器外部的代码放到 jenkins 内部的工作目录下



最关键的有哪些指令:

docker pull :拉取镜像到本地

docker images :列出所有的镜像

docker ps :列出当前系统中正在运行的容器

docker commit :生成镜像

docker build :基于 dockerfile 生成镜像

docker exec-it jenkins bash :进入容器内部

docker run -it :把镜像运行成为实例对象

docker rm -f:删除镜像 docker rmi

exit:退出容器内部环境

docker logs+容器名称:查某个容器的 docker 日志



利用 docker 从0到1发布上线的整个过程：

1、我们要制作本地镜像仓库

2、利用 docker build 的方式基于 docker file 去制作含有网站代码以及各种依赖的前后端 docker 镜像，并利用 docker push 上传到本地仓库中【备份)

3、再利用 docker run 运行前后端镜像，并生成前后端实例

就说明部署成功

4、用户通过网址访问网站，并且接口也有正常响应数据的情况，



你在工作中你怎么用 docker 的：

我工作中没有用到 docker，已经有一套完整的 cd 流水线了，不过我看过相关的学习资料和公司的搭建文档，我知道怎么用的



怎么在这个容器内去执行一些命令：

进入容器内部，这进去之后就可以执行其他命令了docker exec - it jenkins bash可以换成其他的。这里的jenkins 是容器的名称 可以换成别的



docker 怎么去拉一个镜像，怎么把它部署起来：

先 docker pull 镜像，然后再运行 docker run 镜像，最后生成 docker 的实例，就能部署起来了



怎么去 docker 里面去终止掉某个进程：

(先进去，再 kill)

docker exec -it jenkins /bin/bash

kill pid



**你是怎么使用Jenkins的**

​	公司租了一个阿里云的服务器,专门运行jenkins服务Jenkins服务搭建 

​	-**我用的mac 我在终端用 SSH 连接服务 安装 Jenkins 并配置**	**用 scp 命令传输文件**

​	Jenkins服务是我独立搭建的

​	[可选]我们公司主要使用lenkins完成了测试环境的一键部署脚本,脚本的实现过程是首先kil测试环境的后。端进程,移除war包,然后git拉取最新代码进行build,并远程拷贝新的war包到测试环境对应的tomcat中,最后启动tomcat

​	[可选]我们公司的lenkins主要用于CI持续集成

首先是高频检测前后端git仓库的代码变动,如发现代码更新,则触发自动部署测试环境然后再通过git拉去最新的自动化测试代码,执行并生成allure测试报告,生成的测试报告会通过邮件发送给相关人员

​	[可选]在dev分支上经过了自动化测试的代码会被提交到test以便进一步完成系统测试o[可选1我们公司的lenkins还会用于CD持续部署

在验收测试通过之后，Jenkins会通过git把代码合并到主干

然后拉去主干最新代码进行构建,把代码转化为可执行的iar包或war包(或docker镜像)然后执行运维配置好的部署脚本(如果是docker镜像,需通过push上传镜像到镜像仓库,再把镜像运行为实例,同时用到了k8s进行集群部署)

​	[可选]我们公司的jenkins也会用于线上巡检,定时每天凌晨3点运行一次自动化测试



**持续集成CI：在源代码变更后自动检测、拉取、构建的过程。**

**持续交付CD：则是自动化部署和发布的过程，确保代码可以随时可靠地发布到生产环境。**



**了解哪些Jenkins插件：**

​	gitee插件,提供与gitee的集成

​	allure插件,提供在线读取allure测试报告的功能

​	dingtalk插件,提供发送钉钉消息的功能

​	emailextension插件,允许配置和发送通知邮件

​	ssh插件,允许ssh远程连接

​	maven插件,提供对maven项目的支持

​	docker插件,提供与docker的集成,允许操作docker仓库和容器



**怎么在Jenkins查看测试报告：**

​	首先要在jenkins服务器上下载allure,并配置环境变量

​	然后在jenkins中下载allure插件

​	然后通过 构建后操作 就可以执行自动化测试和生成allure报告了

​	可以通过生成在线报告以及在线地址来访问,也可以通过邮件发送离线报告,打开离线报告进行访问



**配置Jenkins过程遇到的错误：**

​	遇到的什么错误这个倒是没有，你可以说是公司有专门的运维来维护Jenkins

​	测试这边一般只是使用Jenkins 



**如何配置Jenkins项目：**

​	首先新建任务,输入项目名称,选择"自由风格项目”

​	然后配置源码管理,构建触发器,构建步骤以及构建后操作即可



**钉钉集成：**

​	首先安装钉钉的插件

​	然后在钉钉群里面创建一个webhook的机器人安装好之后再系统管理里面找到钉钉配置webhook地址和加密在项目里面选择通知谁，什么时候通知，以及自定义消息的内容