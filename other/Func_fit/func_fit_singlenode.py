#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 22:36:54 2018

@author: chaos
"""

import csv
import math
import numpy as np
import argparse
import ast

from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from BinaryRectifyCoefficientWriter import BinaryRectifyCoefficientWriter

def parse_args(check=True):
	## argparse does NOT type bool. Use ast.literal_evaal instead.
    parser = argparse.ArgumentParser(description='A procedure to estimate the coefficients of the temperature curvs')
    
    parser.add_argument("--list_csv_data_files", type=str, default=None,
                        help="The list of the input data files in csv format, seperated by .")
    parser.add_argument("--b_handle_as_one", type=ast.literal_eval, default=True,
                        help="Should we merge all the input data to fit a singe curve.")
    parser.add_argument("--model_types", type=str, default='pow', 
                        help="The fitting fuction for the given data. Options are: poly, pow, exp. This arguments can be a list seperated by comma.")
    parser.add_argument("--show_fitted_func", type=ast.literal_eval, default=True,
                        help="Should we should the fitted curve")
    parser.add_argument("--col_x", type=int, default=2,
                        help="The index of colume of value x in the data file.")
    parser.add_argument("--col_y", type=int, default=0,
                        help="The index of colume of value y in the data file.")
    parser.add_argument("--splitchar", type=str, default=';',
                        help="The index of colume of value y in the data file.")
    parser.add_argument("--rescale_factor", type=float, default=100.0,
                        help="The rescale factor for x in the data file.")
    parser.add_argument("--binary_file_path", type=str, default="rectifymap0.data",
                        help="The rescale factor for x in the data file.")
    
    FLAGS, unparsed = parser.parse_known_args()
    
    return FLAGS, unparsed

def load_data_temperature(filename, splitchar = ';', col_x = 2, col_y = 0, rescale = 100):
    distance = 0
    x, y=[],[]
    with open(filename,'r') as myFile:
        lines=csv.reader(myFile)
        n_lines = 0
        for line in lines:
            print(line)
            # Chaos: Add for rectify map output
            n_lines = n_lines + 1            
            # End
            
            if(';' == splitchar):
                var_lst = line[0].split(splitchar); print(var_lst) # 
            elif (',' == splitchar):
                var_lst = line
            
            # Chaos: Add for rectify map output
            if (1 == n_lines):
                # Parse the distance
                distance = float(var_lst[0])
                continue
            # End
            # The temperature records.
            # Handle it.
            val_x = float(var_lst[col_x]) / rescale
            val_y = float(var_lst[col_y])
            
            x.append(val_x)
            y.append(val_y)
            
            # print(val_x, val_y)
    return x, y, distance

def func_power(x, a, b, c):
    return a * np.power(x, b) + c

def func_expre(x,a,b):
    return a*np.exp(b/x)

def compute_poly_value(x, coeff, order):
    return coeff * np.power(x, order)

def fit_pred(x, coeffs, func_type = 'pow'):
    y = None
    if 'pow' == func_type:
        y = func_power(x, coeffs[0], coeffs[1], coeffs[2])
    elif 'poly' == func_type:
        y = np.polyval(coeffs, x)
#        y = np.zeros([len(x), ])
#        for o_i in range(len(coeffs)):
#            order = len(coeffs) - o_i
#            coeff = coeffs[o_i]
#            
#            y_ = compute_poly_value(x, coeff, order)
#            y += y_
            
    elif 'exp' == func_type:
        y = func_expre(x, coeffs[0], coeffs[1])
    
    return y

def funz_rev(x, a, b, c):
    return math.exp(math.log((x-c)/a)/b)
    
def fit_main(x, y, func_type = 'pow', order=3):
    coeffs = None
    if 'pow' == func_type:
        popt, pcov = curve_fit(func_power, x, y, maxfev=500000)
        coeffs = popt
    elif 'poly' == func_type:
        popt = np.polyfit(x, y, order)
        coeffs = popt
    elif 'exp' == func_type:
        popt, pcov = curve_fit(func_power, x, y, maxfev=5000)
        coeffs = popt
        
    return coeffs

def fit_print(coeffs, func_type = 'pow'):
    line = ''
    if 'pow' == func_type:
        line = "%.09f * pow(x,%.09f) + %.09f"%(coeffs[0], coeffs[1], coeffs[2])
    elif 'poly' == func_type:
        for o_i in range(len(coeffs)):
            order = len(coeffs) - o_i
            
            line_s = "%.09f * x**%d"%(coeffs[o_i], order)
            if o_i != (len(coeffs) - 1):
                line_s += ' + '
            
            line += line_s
    elif 'exp' == func_type:
        line = "%.09f * exp(%.09f / x) + %.09f"%(coeffs[0], coeffs[1])
        
    return line

def main():
    FLAGS, unparsed = parse_args()
    
    if not FLAGS.list_csv_data_files:
        raise ValueError("You must give some data.")
    
    # The output file in binary format.
    filename_binary_o = FLAGS.binary_file_path; print(filename_binary_o)
    
    lst_csv_input  = FLAGS.list_csv_data_files; print(lst_csv_input)
    b_input_merge  = FLAGS.b_handle_as_one; print(b_input_merge)
    lst_model_type = FLAGS.model_types
    b_show_fitted  = FLAGS.show_fitted_func
    
    splitchar = FLAGS.splitchar
    col_x     = FLAGS.col_x
    col_y     = FLAGS.col_y
    rescale_f = FLAGS.rescale_factor
    
    if 1 != len(splitchar):
        raise ValueError('The split char for the input data csv file must be a single visible character')
    
    # Check if the number of parameter of the lst_csv_input and ls_model_type equal
    lst_input_path  = lst_csv_input.split(',')
    lst_input_mtype = lst_model_type.split(',')
    
    if (True == b_input_merge) & (1 != len(lst_input_mtype)):
        raise ValueError('The type of target model must be 1 if you take all data into one model')
    elif (False == b_input_merge) & (len(lst_input_path) != len(lst_input_mtype)):
        raise ValueError('The number of the target model types must be equal to the number of input data files if you want to fit different models')
    
    x_v, y_v, dists = [], [], []
    for filename in lst_input_path:
        x, y, distancx = load_data_temperature(filename, splitchar, col_x, col_y, rescale_f)
        if True == b_input_merge:
            x_v.extend(x)
            y_v.extend(y)
            # Chaos: Add for rectify map output
            dists.extend(distancx)
            # End
        else:
            x_v.append(x)
            y_v.append(y)
            # Chaos: Add for rectify map output
            dists.append(distancx)
            # End
    
    # Fit funcs   
    range_max = 1 if b_input_merge else len(x_v)
    # Or use
    # range_max = b_input_merge and 1 or len(x_v)
    for idx in range(range_max):
        func_type = lst_input_mtype[idx]
        print(func_type)
        if b_input_merge:
            x = x_v
            y = y_v
            distance = dists[0]
        else:
            x = x_v[idx]
            y = y_v[idx]
            distance = dists[idx]
        
        coeffs = fit_main(x, y, func_type)
        # Save the coefficient in to a file.
        BinaryRectifyCoefficientWriter(filename_binary_o, distance, coeffs[0], coeffs[1], coeffs[2])
        
        func_format = fit_print(coeffs, func_type)
        print(func_format)
        
        if b_show_fitted:
            plt.plot(x, y, 'g+', label='original values')
        
            val_w = np.linspace(0, 1000, 1000)
            val_z = fit_pred(val_w, coeffs, func_type)
            
            plt.plot(val_w, val_z, 'r',label=func_format)
            
        if 'pow' == func_type:
            x_pred = [170.0, 180.0, 190.0, 200.0, 210.0]
            y_pred = []
            for x_ in x_pred:
                y_ = funz_rev(x_, coeffs[0], coeffs[1], coeffs[2])
                y_pred.append(y_)
            
            print(y_pred)
            plt.plot(y_pred, x_pred, 'g', label='pred_inv_fit values')
            
        if b_show_fitted:
            plt.xlabel('x axis')
            plt.ylabel('y axis')
            plt.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
            plt.title('curve_fit')
            plt.grid(True)
            plt.xlim(0, 200)
            plt.ylim(0, 200)
            plt.show()

if __name__ == '__main__':
    '''
    Note: You must convert the Excel file into csv format before calling this script.
    Usage:
    python func_fit.py \
        --list_csv_data_files=blackpanel.csv,camera2.csv \
        --b_handle_as_one=False \
        --model_types=pow,poly \
        --show_fitted_func=True \
        --col_x=2 \
        --col_y=0 \
        --splitchar=';' \
        --rescale_factor100
    
    For short, it can be:
    python func_fit.py \
        --list_csv_data_files=blackpanel.csv,camera2.csv \
        --b_handle_as_one=True \
        --model_types=pow \
        --show_fitted_func=True
    '''
    main()
