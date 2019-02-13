# -*- coding: utf-8 -*-
# File : getSongExtList.py
# Author: wangyuan
# mail: wyxidian@gmail.com
# Created Time: 2019/2/10
#!/bin/bash

import urllib2,urllib
import re
import xml.etree.cElementTree as et
import json
import os
import datetime
import time
class HebaXml():
    url = 'http://www.52heba.com:8081/WebService.asmx/SearchSong?jsonStr={{"MemberId":"17802929684"%2C"Page":"{0}"%2C"Flag":-1%2C"PageSize":"10000"%2C"Where":"{1}"}}&key=28f3dabfcf79246b251a746341f41ad3'

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
            urllib.urlretrieve(file_url, filename=filename)
        except IOError as e:
            print '文件操作失败', e
        except Exception as e:
            print '错误 ：', e


    def read_word(self, file_path='./config/hanzi.txt'):
        res = []
        with open(file_path, 'r') as fr:
            for line in fr.readlines():
                line = line.strip()
                if len(line)>0:
                    res.append(line)

        return res

    def getAllItems(self):
        words = self.read_word(file_path='./config/hanzi.txt')
        song_name_set = set()
        res = []
        for idx, word in enumerate(words):
            print 'processing:\t'+word+'\tindex:\t'+str(idx)
            for p in range(1, 1000):
                url = self.url.format(p, word)
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
                    if song['ChineseSongName'] in song_name_set:
                        continue
                    song_name_set.add(song['ChineseSongName'])
                    res.append(item)

                if (idx % 10 == 0):
                    time.sleep(1)
                print 'count:\t' + str(list_num)
                if list_num < 10000:
                    break
        return res
    def getOneItems(self, word = '我'):
        song_name_set = set()
        res = []
        for p in range(1, 1000):
            url = self.url.format(p, word)
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
                if song['ChineseSongName'] in song_name_set:
                    continue
                song_name_set.add(song['ChineseSongName'])
                res.append(item)

            print 'count:\t' + str(list_num)
            if list_num < 10000:
                break
        return res



if __name__ == '__main__':
    # with open("./config/record.json", 'r') as load_f:
    #     load_dict = json.load(load_f)
    # res = HebaXml().getOneItems()
    res = HebaXml().getAllItems()
    with open("./config/record.json", "w") as f:
        json.dump(res, f)
    print("加载入文件完成...")
