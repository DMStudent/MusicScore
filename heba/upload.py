# -*- coding: utf-8 -*-
# File : upload.py
# Author: wangyuan
# mail: wyxidian@gmail.com
# Created Time: 2019/2/9
#!/bin/bash

from bypy import ByPy
import numpy
import os
import cv2 as cv
if __name__ == '__main__':
    res = numpy.load('/search/wangyuan/automatic-watermark-detection/config/para.npy.bkp')
    img = res[1][0]
    cv.imwrite('/search/wangyuan/automatic-watermark-detection/test.png', img)

    path = "./result"
    os.chdir(path)
    bp = ByPy()
    bp.list() # or whatever instance methods of ByPy class
    # bp.mkdir('heba/origin')
    # bp.rm('v6')
    # bp.upload(bypy.tgz)
    bp.syncup(u'./', u'heba/origin')
    print "fineshed!!!"




