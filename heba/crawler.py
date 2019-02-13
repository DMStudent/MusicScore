# -*- coding: utf-8 -*-
# File : crawler.py
# Author: wangyuan
# mail: wyxidian@gmail.com
# Created Time: 2019/2/9
#!/bin/bash

import urllib2,urllib
import re
import xml.etree.cElementTree as et
import json
import os
import datetime

class HebaXml():
    url = 'http://www.52heba.com:8081/WebService.asmx/GetRecommendSongList?jsonStr={{"MemberId":"17802929684","Page":{0},"PageSize":20,"Where":""}}&key=a117ec2d9c91a7ecd81673d56f96d2c6'
    pattern_item = re.compile(r'<item>\s*?<title>(.*?)</title>\s*?<summary>(.*?)</summary>\s*?<link>(.*?)</link>')

    def dict2str(self, d):
        res = ""
        for k, v in d.items():
            res += k + ":\t" + unicode(v) + "\n"
        return res.strip()

    def save_resoure(self, file_url, file_path='./result/'):
        # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
        try:
            # 获得图片后缀
            file_suffix = file_url.split('/')[-1]
            # 拼接图片名（包含路径）
            filename = '{}{}{}'.format(file_path, os.sep, file_suffix)
            # 下载图片，并保存到文件夹中
            print 'downloading:'+file_url
            if len(file_suffix) > 0:
                urllib.urlretrieve(file_url, filename=filename)
        except IOError as e:
            print '文件操作失败', e
        except Exception as e:
            print '错误 ：', e


    def getItems(self, page=1):
        url = self.url.format(page)
        content = urllib2.urlopen(url).read()
        root = et.fromstring(content)
        # 获取标签名字
        js_content = root.text
        js_content = json.loads(js_content)
        if not js_content:
            return None

        song_list = js_content['SongExtList']
        list_num = len(song_list)

        for i in range(list_num):
            item = song_list[i]
            song = item['Song']
            print i, song['ChineseSongName']
            file_path = u'./result/'+song['ChineseSongName']
            file_path = file_path.encode("utf-8")
            if os.path.isdir(file_path):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
                print 'dir exists'
                continue
            else:
                print 'dir not exists'
                os.mkdir(file_path)  ##只能创建单级目录，用这个命令创建级联的会报OSError错误         print 'mkdir ok

            with open(file_path+"/readme.txt", 'w') as fw:
                fw.write(self.dict2str(song).encode("utf-8"))
            download_url = song['DownloadUrl'].encode('utf-8')
            song_url = 'http://www.52heba.com:8080/' + download_url
            self.save_resoure(song_url, file_path=file_path)

            open_list = item['OpernList']
            for j in range(len(open_list)):
                download_url = open_list[j]['DownloadUrl'].encode('utf-8')
                img_url = 'http://www.52heba.com:8080/' + download_url
                self.save_resoure(img_url, file_path=file_path)

    def getItemsFromList(self, song_list):
        list_num = len(song_list)
        for i in range(list_num):
            item = song_list[i]
            song = item['Song']
            print i, song['ChineseSongName']
            file_path = u'./result/'+song['ChineseSongName']
            file_path = file_path.encode("utf-8")
            if os.path.isdir(file_path):  ##不用加引号，如果是多级目录，只判断最后一级目录是否存在
                print 'dir exists'
                continue
            else:
                print 'dir not exists'
                os.mkdir(file_path)  ##只能创建单级目录，用这个命令创建级联的会报OSError错误         print 'mkdir ok

            with open(file_path+"/readme.txt", 'w') as fw:
                fw.write(self.dict2str(song).encode("utf-8"))
            download_url = song['DownloadUrl'].encode('utf-8')
            song_url = 'http://www.52heba.com:8080/' + download_url
            self.save_resoure(song_url, file_path=file_path)

            open_list = item['OpernList']
            for j in range(len(open_list)):
                download_url = open_list[j]['DownloadUrl'].encode('utf-8')
                img_url = 'http://www.52heba.com:8080/' + download_url
                self.save_resoure(img_url, file_path=file_path)

if __name__ == '__main__':
    with open("./config/record.json", 'r') as load_f:
        song_list = json.load(load_f)
    ref_day = datetime.date(2019, 2, 10)
    today = datetime.date.today()
    diff_day = today - ref_day
    page = diff_day.days
    begin = 50*page
    end = min(50*(page+1), len(song_list))
    if begin > end:
        print 'over!'
        song_list = []
    else:
        song_list = song_list[begin:end]
    # print page
    HebaXml().getItemsFromList(song_list)