"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: na_populations.py
@time: 18/12/2017 10:41 PM
"""
from pygal_maps_world.maps import World

wm = World()

wm._title = 'Populations of Countries in North America'
wm.add('North America', {'ca':34126000, 'us':309349000, 'mx':113423000})

wm.render_to_file('na_populations.svg')
