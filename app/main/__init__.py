# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:43:14 2016

@author: david
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
