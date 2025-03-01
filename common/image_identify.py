from PIL import Image
import ddddocr


def image_identify(driver, ele, whole_name, crop_name):
    """
    :param driver: 浏览器驱动
    :param ele: 验证码的元素
    :param whole_name: 整个页面的截图名字
    :param crop_name:  页面中对于验证码的抠图名字
    :return: 返回验证码识别出来的字符串
    """
    driver.save_screenshot(whole_name)
    left = ele.location['x']
    top = ele.location['y']
    right = ele.size['width'] + left
    height = ele.size['height'] + top

    img = Image.open(whole_name).crop((left, top, right, height))
    img.save(crop_name)

    ocr = ddddocr.DdddOcr()
    with open(crop_name, 'rb') as f:
        image = f.read()
    res = ocr.classification(image)
    print(res)
    return res
