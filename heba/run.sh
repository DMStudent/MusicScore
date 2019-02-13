# -*- coding: utf-8 -*-                                                                                                              
#########################################################################
# File Name: run.sh
# Author: wangyuan
# mail: wangyuan214159@sogou-inc.com
# Created Time: 2019年02月10日 星期日 10时11分43秒
#########################################################################
#!/bin/bash
bin=`dirname $0` 
cd ${bin}

/search/anaconda/envs/py2/bin/python getSongExtList.py
/search/anaconda/envs/py2/bin/python crawler.py
/search/anaconda/envs/py2/bin/python pic2pdf.py
/search/anaconda/envs/py2/bin/python upload.py
