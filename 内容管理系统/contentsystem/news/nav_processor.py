"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: nav_process.py
@time: 29/12/2017 9:38 PM
上下文渲染器
"""
from .models import Column

nav_display_columns = Column.objects.filter(nav_display=True)


def nav_column(request):
    return {'nav_display_columns': nav_display_columns}
