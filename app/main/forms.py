# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:03:00 2016

@author: david
"""
from flask import request, make_response, url_for, current_app
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
import os, random, datetime

"""
更换成从 Form 和 EditForm 继承
class PostForm(Form):
    body = TextAreaField(u'想说点什么？', validators=[Required()])
    submit = SubmitField(u'提交')
"""
    
class LoginForm(Form):
    username = StringField(u'用户名或Email', validators=[Required(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'提交')
    

class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField(u'密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入密码必须匹配')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'提交')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
            

class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[
        Required(), EqualTo('password2', message=u'两次输入新密码必须匹配')])
    password2 = PasswordField(u'再次输入确认新密码', validators=[Required()])
    submit = SubmitField(u'更新密码')


class EditProfileForm(Form):
    signature = StringField(u'个性签名', validators=[Length(0, 64)])
    location = StringField(u'地点', validators=[Length(0, 64)])
    about_me = TextAreaField(u'关于我')
    submit = SubmitField('Submit')


class CKEditor(object):
    def __init__(self):
        pass

    def gen_rnd_filename(self):
        """generate a random filename"""
        filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))

    def upload(self, endpoint=current_app):
        """img or file upload methods"""
        error = ''
        url = ''
        callback = request.args.get("CKEditorFuncNum")

        if request.method == 'POST' and 'upload' in request.files:
            # /static/upload
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            rnd_name = '%s%s' % (self.gen_rnd_filename(), fext)

            filepath = os.path.join(endpoint.static_folder, 'upload', rnd_name)

            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                    error = 'ERROR_DIR_NOT_WRITEABLE'
            if not error:
                fileobj.save(filepath)
                url = url_for('main.static', filename='%s/%s' % ('upload', rnd_name))
        else:
            error = 'post error'

        res = """
                <script type="text/javascript">
                window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
                </script>
             """ % (callback, url, error)

        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response
        

class PostForm(Form, CKEditor):
    body = TextAreaField(u'编辑你的主题')
    submit = SubmitField('submit')
    
class CommentForm(Form):
    body = StringField(u'添加你的评论', validators=[Required()])
    submit = SubmitField('Submit')