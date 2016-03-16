# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:43:14 2016

@author: david
"""
from flask import Blueprint

## 此处要加参数 static_folder, 在图片上传时会用到静态 static 路径
main = Blueprint('main', __name__, static_folder='', template_folder='templates', static_url_path='')

from . import views, errors
