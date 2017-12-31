"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: urls.py
@time: 30/12/2017 8:37 PM
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # 类视图用as_view()方法将类转换为函数
    url(r'^$', views.IndexView.as_view(), name='index'),
    # 类视图方法
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    # url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    # 类视图方法
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    # url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    # 类视图方法
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    # 搜索
    # url(r'^search/$', views.search, name='search'),

]