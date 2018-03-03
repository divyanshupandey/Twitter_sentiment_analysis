#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 17:55:49 2018

@author: user
"""
# importing necessary libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
style.use('fivethirtyeight')

#setting graph for pie chart
fig1 = plt.figure(1, figsize=(6, 6))
ax = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
classes = ["positive","negative","neutral"]

#setting graph for line chart
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

#plotting both the graphs   
def pie_plot(i):
    xs = []
    ys = []
    value = []
    
    #using file data for preparing graphs
    file_data  = open('prediction_files/output.txt','r').read()
    predict_data  = open('prediction_files/prediction.txt','r').read()
    
    if(file_data == ""):
        value.append(1)
        value.append(1)
        value.append(1)

    else:
        for val in file_data.split(","):
            value.append(int(val))
            
    if(predict_data != ""):
        for val in predict_data.split("\n"):
            if val != "":
                xs.append(int(val.split(",")[0]))
                ys.append(int(val.split(",")[1]))
        
    #plotting both the graphs
    ax1.clear()
    ax1.plot(xs, ys)
    ax.clear()
    pies = ax.pie(value,colors=['g','r','c'], labels=classes, autopct='%1.1f%%')
  
ani = animation.FuncAnimation(fig1, pie_plot, interval=1000)
ani1 = animation.FuncAnimation(fig, pie_plot, interval=1000)
plt.show()