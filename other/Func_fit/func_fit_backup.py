#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 22:36:54 2018

@author: chaos
"""

import csv
import math
import numpy as np

from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

def load_data_temperature(filename):
    x, y=[],[]
    with open(filename,'r') as myFile:
        lines=csv.reader(myFile)
        for line in lines:
            # print(line)
            var_lst = line[0].split(';')
            val_x = float(var_lst[2]) / 100
            val_y = float(var_lst[0])
            
            x.append(val_x)
            y.append(val_y)
            
            # print(val_x, val_y)
    return x, y    

def funz(x, a, b, c):
    return a * pow(x, b) + c

def func(x,a,b):
    return a*np.exp(b/x)

x, y = load_data_temperature('camera2.csv')
# x_l, y_l = load_data_temperature('low-temp.csv')
# x_l = np.multiply(x_l, 100.0)
# plot5=plt.plot(x_l, y_l, 'g+', label='lower values')

# x.extend(x_l)
# y.extend(y_l)
# Draw dots
# plt.plot(x, y)

cofs = np.polyfit(x, y, 3)
print(cofs)

val_w = np.linspace(0, 1000, 1000)
val_z = np.polyval(cofs, val_w)#根据多项式求函数值
plot2=plt.plot(val_w, val_z, 'r',label='polyfit values')
plot1=plt.plot(x, y, '*',label='original values')
plt.grid(True)
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('polyfitting')
plt.xlim(0, 200)
plt.ylim(0, 200)
#plt.show()
# plt.save('poly-fit.png')



popt, pcov = curve_fit(funz, x, y, maxfev=5000)
a=popt[0]#popt里面是拟合系数，读者可以自己help其用法
b=popt[1]
c=popt[2]

print(popt)

yvals=funz(val_w,a,b,c) # )#
# print(yvals)
# plot1=plt.plot(x, y, '*',label='original values')
plot3=plt.plot(val_w, yvals, 'b',label='power_fit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('curve_fit')
plt.grid(True)
plt.xlim(0, 200)
plt.ylim(0, 200)
#plt.show()

def funz_rev(x, a, b, c):
    return math.exp(math.log((x-c)/a)/b)

x_pred = [170.0, 180.0, 190.0, 200.0, 210.0]
y_pred = []
for x_ in x_pred:
    y_ = funz_rev(x_, a, b, c)
    y_pred.append(y_)
    
print(y_pred)
plot4=plt.plot(y_pred, x_pred, 'g', label='pred_inv_fit values')

plt.xlabel('x axis')
plt.ylabel('y axis')
plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
plt.title('curve_fit')
plt.grid(True)
plt.xlim(0, 200)
plt.ylim(0, 200)
plt.show()
