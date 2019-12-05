# -*- coding: utf-8 -*-
# @Time    : 2019/12/5 11:14
# @Author  : King life
# @Email   : 18353626676@163.com
# @File    : captch_handles.py
# @Software: PyCharm
import os
import time
from collections import Counter

from PIL import Image
from tqdm import tqdm


def category_captch():
    """
    这个是将1000张图片根据上下左右四个角的像素进行分类，因为4个角一般不会被缺口覆盖
    代码中的259，115是整个图片像素size(260, 116)的顶点坐标，不能写到260、116，会报错
    """
    for i in range(1000):
        image_path = "./notch_image/new_image{}.png".format(i)
        image = Image.open(image_path)
        pixel1 = image.getpixel((0, 0))
        pixel2 = image.getpixel((259, 0))
        pixel3 = image.getpixel((0, 115))
        pixel4 = image.getpixel((259, 115))
        hash_result = hash(pixel1 + pixel2 + pixel3 + pixel3)
        if not os.path.exists("./image_{}".format(hash_result)):
            os.mkdir("./image_{}".format(hash_result))
        image.save("./image_{}/{}.png".format(hash_result, i))


def get_complete_captch():
    """
    获取完整的不带缺口的图片，主要是遍历每个分类的前三十张图片的各个位置像素
    得到同一位置出现次数最多的像素，合成一张完整的图片
    """
    start_time = time.time()
    image_dir_list = ["./image_3266946314994177155", "./image_-4289929732924985292", "./image_-4780728855187118442", "./image_5269397631110749829"]
    for index, image_dir in enumerate(image_dir_list):
        image_path_list = os.listdir(image_dir)[0:30]  # 切片用30张图片足够还原一张完整的图片了
        complete_image = Image.new("RGB", (260, 116))
        # 先打开30张图片保存在列表中
        image_list = [Image.open("{}/{}".format(image_dir, i)) for i in image_path_list]

        for left in tqdm(range(0, 260)):
            # 注意get以及put位子像素不能指定顶点位子（260，116），会报错
            for down in range(0, 116):
                pixels = []
                pixel_tuple = (left, down)
                for item in image_list:
                    pixels.append(item.getpixel((left, down)))  # 获取位置像素
                count = Counter(pixels)  # 获取pixels列表里面每个元素出现的次数
                most_count_pixel = count.most_common(1)[0][0]  # 获取出现次数最高的元素的值
                complete_image.putpixel(pixel_tuple, most_count_pixel)  # 写入位置像素

        complete_image.save("./complete{}.png".format(index))  # 保存图片的时候按下标保存，方便读取
    stop_time = time.time()
    print(stop_time - start_time)


if __name__ == '__main__':
    category_captch()
    get_complete_captch()