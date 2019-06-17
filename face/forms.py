# -*- coding:utf-8 -*-
# Author: cmzz
# @Time :2019/6/5

# 验证码form & 注册表单form
from django import forms


# 注册的form
from face.models import User


class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致。
    username = forms.CharField(required=True)
    # email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
    picture = forms.CharField()


    # image = forms.ImageField(required=False, max_length=10000)


# 登录的form
class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    # 密码不能小于5位
    # password = forms.CharField(required=True, min_length=5)

# 上传图片的form
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['image', ]
