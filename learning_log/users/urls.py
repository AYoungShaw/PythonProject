"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: urls.py
@time: 28/12/2017 7:07 PM
为应用程序users定义url模式
"""
from django.conf.urls import url

from django.contrib.auth.views import login

from . import views

urlpatterns = [
    # 登录页面
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
    # 注销
    url(r'^logout/$', views.logout_view, name='logout'),
    # 注册页面
    url(r'register/$', views.register, name='register'),
]