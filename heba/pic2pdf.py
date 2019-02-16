# -*- coding: utf-8 -*-
# File : pic2pdf.py
# Author: wangyuan
# mail: wyxidian@gmail.com
# Created Time: 2019/2/10
#!/bin/bash

from PIL import Image
import os
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import cv2
import numpy as np

def pic2pdf(input_path, output_path):
    if not os.path.isdir(input_path):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
        print 'picture file input dir do not exists:' + input_path
        return None

    file_list = os.listdir(input_path)
    suffix = input_path.split('/')[-1]
    pdf_name = output_path + '/' + suffix + '.pdf'
    if os.path.isdir(pdf_name):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
        print 'pdf file exists:' + pdf_name
        return None
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            if water_mark(input_path + '/' + x, output_path + '/' + x):
                pic_name.append(x)

    if len(pic_name)<1:
        return
    im1 = Image.open(output_path + '/' + pic_name[0])
    pic_name.pop(0)
    for i in pic_name:
        img = Image.open(output_path + '/' + i)
        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    print("输出文件名称：", pdf_name)

def delete_pics(input_path):
    if not os.path.isdir(input_path):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
        return None

    file_list = os.listdir(input_path)
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            os.remove(input_path + '/' + x)

def pic2pdf_list(song_list):
    list_num = len(song_list)
    for i in range(list_num):
        item = song_list[i]
        song = item['Song']
        print i, song['ChineseSongName']
        input_path = u'./result/' + song['ChineseSongName']
        output_path = u'./pdf/' + song['ChineseSongName']
        input_path = input_path.encode("utf-8")
        output_path = output_path.encode("utf-8")

        if os.path.isdir(output_path):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
            print 'dir exists'
            continue
        else:
            print 'dir not exists'
            os.mkdir(output_path)  ##只能创建单级目录，用这个命令创建级联的会报OSError错误         print 'mkdir ok
        pic2pdf(input_path, output_path)
        delete_pics(output_path)



def water_mark(input_path, output_path):
    img = cv2.imread(input_path)
    if img == None:
        return False

    # 图片二值化处理，把[240, 240, 240]~[255, 255, 255]以外的颜色变成0
    thresh = cv2.inRange(img, np.array([225, 225, 225]), np.array([240, 240, 240]))

    # 创建形状和尺寸的结构元素
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=1)
    # 扩张待修复区域
    kernel = np.ones((3, 3), np.uint8)
    hi_mask = cv2.dilate(erosion, kernel, iterations=1)
    # specular = cv2.inpaint(img, hi_mask, 2, flags=cv2.INPAINT_TELEA)
    # specular = cv2.inpaint(img, hi_mask, 0, flags=cv2.INPAINT_NS)

    # cv2.imwrite('yp-specular.jpg', specular)
    # cv2.imwrite('yp-thresh.jpg', thresh)
    # cv2.imwrite('yp-erosion.jpg', erosion)
    # cv2.imwrite('yp-mask.jpg', hi_mask)

    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            if hi_mask[row, col] != 0:
                img[row, col, 0] = 255
                img[row, col, 1] = 255
                img[row, col, 2] = 255

    cv2.imwrite(output_path, img)
    return True


if __name__ == '__main__':
    water_mark("/search/wangyuan/heba/34.png", "11")
    with open("./config/record.json", 'r') as load_f:
        song_list = json.load(load_f)
    ref_day = datetime.date(2019, 2, 13)
    today = datetime.date.today()
    diff_day = today - ref_day
    page = diff_day.days
    begin = 300*page
    end = min(300*(page+1), len(song_list))
    if begin > end:
        print 'over!'
        song_list = []
    else:
        song_list = song_list[begin:end]
    pic2pdf_list(song_list)
    # print page
