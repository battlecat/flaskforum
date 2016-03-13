# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 22:03:00 2016

@author: david
"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError

class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
    
class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')