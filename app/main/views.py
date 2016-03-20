# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:24:13 2016

@author: david
"""

from flask import render_template, redirect, url_for, abort, flash, request, current_app
from . import main
from .forms import PostForm, LoginForm, RegistrationForm, ChangePasswordForm,\
         EditProfileForm, CommentForm
from flask.ext.login import current_user, login_user, login_required, logout_user
from ..models import Post, User, Comment
from .. import db
import os
from werkzeug import secure_filename
from PIL import Image



@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)
    

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
            db.session.commit()
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
        db.session.commit()
        flash(u'你的个人资料已经更新')
        return redirect(url_for('.user', username=current_user.username))
    form.signature.data = current_user.signature
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
    

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash(u'评论成功')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


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
        db.session.commit()
        flash(u'文章已经被修改')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/edit-new-post', methods=['GET', 'POST'])
@login_required
def edit_new():
    if not current_user.is_authenticated:
        flash(u'请先登录')
        return redirect(url_for('main.login'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash(u'添加文章成功!')
        return redirect(url_for('main.index'))
 #       return redirect(url_for('.edit', id=post.id))
    return render_template('edit_post.html', form=form)


@main.route('/delete-post/<int:id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(u'文章已经被删除')
    return redirect(url_for('main.index'))
    
@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash(u'你关注了 %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash(u'你取消了对 %s 的关注.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"的关注者",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title=u"关注的人",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif'])


@main.route('/edit-avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    if request.method == 'POST':
        file = request.files['file']
        size = (40, 40)
        im = Image.open(file)
        im.thumbnail(size)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            im.save(os.path.join(main.static_folder, 'avatar', filename))
            current_user.new_avatar_file = url_for('main.static', filename='%s/%s' % ('avatar', filename))
            current_user.is_avatar_default = False
            db.session.add(current_user)
            db.session.commit()
            flash(u'头像修改成功')
            return redirect(url_for('.user', username=current_user.username))
    return render_template('change_avatar.html')

