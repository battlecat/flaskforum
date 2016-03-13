# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:24:13 2016

@author: david
"""

from flask import render_template, redirect, url_for, abort, flash
from . import main
from .forms import PostForm, LoginForm
from flask.ext.login import current_user
from ..models import Post
from .. import db

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
#    posts = Post.query.order_by(Post.timestamp.desc()).all()
#    posts = None
    return render_template('login.html', form=form)