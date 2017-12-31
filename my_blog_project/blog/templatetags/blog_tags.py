"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: blog_tags.py
@time: 30/12/2017 9:14 PM
这里存放自定义模板标签代码
"""
from django import template
# 统计分类
from django.db.models.aggregates import Count
from .. models import Post, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]
# 这样就可以在模板中使用语法{% get_recent_posts %} 来调用这个函数了


@register.simple_tag
def archives():
    return Post.objects.datetimes('created_time', 'month', order='DESC')
# dates返回一个列表，列表中的元素为每一篇文章的创建时间，且是date对象，精确到月份，降序排序


@register.simple_tag
def get_categories():
    # 统计各个分类下的文章数
    # 接收Category相关联的模型post，
    # 统计Category记录的集合中每条记录下的与之关联的post记录的行数
    # 最后把值保存到num_posts属性中
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

    # return Category.objects.all()


@register.simple_tag
def get_tag():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)