"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: countries.py
@time: 18/12/2017 10:21 PM
"""
from pygal_maps_world.i18n import COUNTRIES

for country_code in sorted(COUNTRIES.keys()):
    print(country_code, COUNTRIES[country_code])