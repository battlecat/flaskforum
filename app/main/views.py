# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:24:13 2016

@author: david
"""

from flask import render_template, redirect, url_for, abort, flash, request, current_app
from . import main
from .forms import PostForm, LoginForm, RegistrationForm, ChangePasswordForm,\
         EditProfileForm
from flask.ext.login import current_user, login_user, login_required, logout_user
from ..models import Post, User
from .. import db



@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(u'请先登录')
            return redirect(url_for('main.login'))
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)
    

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)
    

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 在用户会话中标记用户为已登录
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'无效的用户名或密码')
    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(u'注册成功！请登录')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)
    

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经退出。')
    return redirect(url_for('main.index'))
    
@main.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'您的密码已经更新')
            return redirect(url_for('main.index'))
        else:
            flash(u'密码错误，请重试')
    return render_template("change_password.html", form=form)
    
    
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.signature = form.signature.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'你的个人资料已经更新')
        return redirect(url_for('.user', username=current_user.username))
    form.signature.data = current_user.signature
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
    

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    form = PostForm()
    response = form.upload(endpoint=main)
    return response


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)
