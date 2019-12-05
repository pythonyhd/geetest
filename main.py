# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 11:01
# @Author  : King life
# @Email   : 18353626676@163.com
# @File    : main.py
# @Software: PyCharm
"""
w3cschool，注册极验验证码破解
"""
import re
from io import BytesIO

from PIL import Image
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
s = requests.Session()


def get_notch_image():
    """
    根据打乱的图片还原带缺口的图片
    :return:
    """
    response = s.get("https://www.w3cschool.cn/register", headers=headers)
    img_url = "https://www.w3cschool.cn" + re.search(r'background-image: url\("(.+?).png', response.content.decode()).group(1) + ".png"
    img_response = s.get(img_url, headers=headers)
    memory = BytesIO()
    # 把图片暂时写入内存
    memory.write(img_response.content)
    style_sizes = re.findall(r'<div class="gt_cut_fullbg_slice" style="background-position:(.+?);"></div>', response.content.decode())
    style_size_list = []
    for style_size in style_sizes:
        style_size_list.append(tuple([abs(int(i)) for i in re.sub("px", "", style_size).split(" ")]))
    img = Image.open(memory)
    img_size = img.size  # 图片尺寸元祖
    img_mode = img.mode  # 图片模式
    notch_image = Image.new(img_mode, img_size)
    crop_left = 0
    crop_up = 0

    for index, style in enumerate(style_size_list):
        if index < 20:
            small_img = img.crop((style[0], style[1], style[0] + 13, style[1] + 58))
            notch_image.paste(small_img, (crop_left, crop_up))
            crop_left += 13
        elif index == 20:
            crop_left = 0
            crop_up = 58
            small_img = img.crop((style[0], style[1], style[0] + 13, style[1] + 58))
            notch_image.paste(small_img, (crop_left, crop_up))
        else:
            crop_left += 13
            small_img = img.crop((style[0], style[1], style[0] + 13, style[1] + 58))
            notch_image.paste(small_img, (crop_left, crop_up))
    return notch_image


def get_notch(notch_image):
    """
    获取缺口位置
    :param notch_image: 带缺口的图片
    :return:
    """
    notch_image_hash_result = hash(notch_image.getpixel((0, 0)) + notch_image.getpixel((259, 0)) + notch_image.getpixel((0, 115)) + notch_image.getpixel((259, 115)))
    for i in range(4):
        complete_image = Image.open("./complete{}.png".format(i))
        complete_image_hash_result = hash(complete_image.getpixel((0, 0)) + complete_image.getpixel((259, 0)) + complete_image.getpixel((0, 115)) + complete_image.getpixel((259, 115)))
        if notch_image_hash_result == complete_image_hash_result:
            for left in range(0, 260):
                for down in range(0, 116):
                    pixel = (left, down)
                    if notch_image.getpixel(pixel) != complete_image.getpixel(pixel):

                        return pixel


def drag_check(point):
    """
    验证滑块位置是否能请求成功
    :param point: 缺口左上角的X轴像素
    :return:
    """
    post_data = {
        "point": point
    }
    response = s.post("https://www.w3cschool.cn/dragcheck", headers=headers, data=post_data)
    print(response.json())


if __name__ == '__main__':
    for i in range(10):
        notch_image = get_notch_image()
        notch_pixel = get_notch(notch_image)
        print("缺口坐标为：{}".format(notch_pixel))
        drag_check(notch_pixel[0])
