# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:03:00 2016

@author: david
"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField
from wtforms.validators import Required, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class PostForm(Form):
    body = TextAreaField(u'想说点什么？', validators=[Required()])
    submit = SubmitField(u'提交')
    
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
    
