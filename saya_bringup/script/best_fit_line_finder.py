#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def plot_graphs(x1,y1,x2,y2,x_best_fit_1,y_best_fit_1,x_best_fit_2, y_best_fit_2,slope1,intercept1,slope2,intercept2):
    plt.subplot(1, 2, 1)
    plt.title('Slope: ' + str(slope1) + ' / Intercept: ' + str(intercept1))
    plt.plot(x1,y1)
    plt.plot(x_best_fit_1,y_best_fit_1)
    plt.subplot(1, 2, 2)
    plt.title('Slope: ' + str(slope2) + ' / Intercept: ' + str(intercept2))
    plt.plot(x2,y2)
    plt.plot(x_best_fit_2, y_best_fit_2)
    plt.show()

def find_angle(x,y):
    x = [10,9]
    y = [10,10.01]
    m, b = np.polyfit(x, y, 1)
    angle = np.arctan(m)
    if x[0] > x[-1]:
        angle = np.pi + angle
    if angle < 0.0:
        angle = 2*np.pi + angle
    return(m,b)

def generate_curve(power_value, direction):
    x=np.arange(25)
    y=[]
    for i in range(25):
        y.append(direction * (i**power_value))
    return (x,y)

def generate_best_fit_line(slope, intercept):
    x=np.arange(25)
    for i in range(25):
        y=(slope*x)+intercept
    return(x,y)

def main():
    #Variables
    power_value_1 = 2
    power_value_2 = 2

    #Generate Curves
    x1,y1 = generate_curve(power_value_1, 1)
    x2,y2 = generate_curve(power_value_2, -1)

    #Find Slope and Intercept
    slope1,intercept1 = find_angle(x1,y1)
    slope2,intercept2 = find_angle(x2,y2)

    #Generate Best Fit Line
    x_best_fit_1, y_best_fit_1 = generate_best_fit_line(slope1,intercept1)
    x_best_fit_2, y_best_fit_2 = generate_best_fit_line(slope2,intercept2)

    #Plot Graph
    plot_graphs(x1,y1,x2,y2,x_best_fit_1,y_best_fit_1,x_best_fit_2, y_best_fit_2,slope1,intercept1,slope2,intercept2)

if __name__=='__main__':
    main()