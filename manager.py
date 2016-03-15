# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 21:25:12 2016

@author: david
"""

import os
from app import create_app, db
from app.models import User, Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import re

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def subImg(name):
    re_img = re.compile('<img.*?/>')
    return re.sub(re_img, u'[图片]', name)
    
env=app.jinja_env
env.filters['subImg'] = subImg

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()