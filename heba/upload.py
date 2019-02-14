# -*- coding: utf-8 -*-
# File : upload.py
# Author: wangyuan
# mail: wyxidian@gmail.com
# Created Time: 2019/2/9
#!/bin/bash

from bypy import ByPy
import os
def upload(local, remote):
    #os.chdir(local)
    bp = ByPy()
    bp.list() 
    bp.syncup(local, remote)
    print "fineshed!!!"



if __name__ == '__main__':
    local = u"./result"
    remote = u"heba/origin"
    upload(local, remote)
    local = u"./pdf"
    remote = u"heba/pdf"
    upload(local, remote)

