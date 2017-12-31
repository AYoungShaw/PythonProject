"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: forms.py
@time: 30/12/2017 9:59 PM
进行表单设计
"""

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    表单必须继承自forms.Form或者forms.modelForm
    如果表单对应一个数据库模型，用modelForm会简单很多
    """
    class Meta:
        model = Comment
        # 指定了表单的字段
        fields = ['name', 'email', 'url', 'text']