"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: urls.py
@time: 26/12/2017 11:04 PM
定义learning_logs的URL模式
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    # 主页
    # 第一个参数是url的正则模式，
    # 第二个参数是view中的视图函数，
    # 第三个参数是URL模式的名称。指定为index。可以在代码的其他地方引用它
    url(r'^$', views.index, name='index'),
    # 显示所有主题
    url(r'^topic/$', views.topics, name='topics'),
    # 特定主题的详细页面
    # /(?P<topic_id>\d+)/ 整数匹配，将匹配的值放入到topic_id中
    url(r'^topic/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # 用于添加新主题的网页
    url(r'^new_topc/$', views.new_topic, name='new_topic'),
    # 用于添加新条目的页面
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # 用于编辑条目的页面
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),

]
