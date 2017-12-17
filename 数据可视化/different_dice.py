"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: different_dice.py
@time: 17/12/2017 10:04 PM
"""
from die import Die

import pygal

# 创建一个D6和一个D10
die_1 = Die()
die_2 = Die(10)

# 掷骰子多次，并将结果存储到一个列表
results = []

for roll_num in range(50000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

# 分析结果
frequencies = []
max_result = die_1.num_sides + die_2.num_sides

for value in range(2, max_result + 1):
    frequency = results.count(value)
    frequencies.append(frequency)

# 可视化结果
hist = pygal.Bar()

hist._title = "Result of rolling a D6 and a D10 50,000 times."
hist.x_labels = ['2', '3', '4', '5', '6', '7', '8', '9',
                 '10', '11', '12', '13', '14', '15', '16']


hist._x_title = 'Result'
hist._y_title = 'Frequency of Result'

hist.add('D6 + D10', frequencies)
hist.render_to_file('dice_visual1.svg')