"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: country_codes.py
@time: 18/12/2017 10:29 PM
"""
from pygal_maps_world.i18n import COUNTRIES


def get_country_code(country_name):
    '''根据指定的国家，返回Pygal使用的两个字母的国别码'''
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code

        # 如果没有找到
    return None

