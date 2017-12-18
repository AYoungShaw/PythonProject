"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: americas.py
@time: 18/12/2017 10:35 PM
"""
from pygal_maps_world.maps import World

wm = World()
wm._title = 'North, Central, and South America'

wm.add('North Amerca', ['ca', 'mx', 'us'])
wm.add('Central America', ['bz', 'cr', 'gt', 'hn', 'ni', 'pa', 'sv'])
wm.add('South America', ['ar', 'bo', 'br', 'cl', 'co', 'ec',
                         'gf', 'gy', 'pe', 'py', 'sr', 'uy', 've'])

wm.render_to_file('americas.svg')