"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: forms.py
@time: 28/12/2017 2:36 PM
这里是创建表单
"""
# 创建表单需要导入forms包
from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    # 最简单的Modelform只包含一个内嵌的Meta类
    # 告诉Django根据哪个模型创建表单，以及在表单中包含的哪些字段
    class Meta:
        # 包含的模型
        model = Topic
        # 包含的字段
        fields = ['text']
        # 不用为字段生成标签
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # 小部件(widgets)是一个HTML表单元素，如单行文本框，多行文本区域或下拉列表
        # 将文本区域宽度设置为80列
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
