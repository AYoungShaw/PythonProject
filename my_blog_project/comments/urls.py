"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: urls.py
@time: 30/12/2017 10:21 PM
"""

from django.conf.urls import url

from . import views
# 命名空间
# app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]