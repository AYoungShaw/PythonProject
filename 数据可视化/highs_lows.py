"""
@author: MrYang 
@contact: Shaw_Yang@163.com
@site: www.example.com
@file: highs_lows.py
@time: 17/12/2017 10:18 PM
"""
import csv

from datetime import datetime

from matplotlib import pyplot as plt

# 从文件中获取数据
# filename = 'sitka_weather_07-2014.csv'

# filename = 'sitka_weather_2014.csv'

filename = 'death_valley_2014.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

# for index, column_header in enumerate(header_row):
#     print(index, column_header)

    dates,  hights, lows = [], [], []
    for row in reader:
        try:
            current_date = datetime.strptime(row[0], '%Y-%m-%d')

            high = int(row[1])
            low = int(row[3])

        except ValueError:
            print(current_date, 'missing data')
        else:
            dates.append(current_date)
            hights.append(high)
            lows.append(low)

    # print(hights)

# 根据数据绘制图形
fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, hights, c='red', alpha=0.5)
plt.plot(dates, lows, c='red', alpha=0.5)
plt.fill_between(dates, hights, lows, facecolor='blue', alpha=0.1)

# 设置图形的格式
# plt.title("Daily high temperatures, July 2014", fontsize=24)
title = 'Daily high temperatures - 2014\nDeath Valley, CA'
plt.title(title, fontsize=20)
plt.xlabel('', fontsize=16)

fig.autofmt_xdate()

plt.ylabel('Temperature (F)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)

plt.show()