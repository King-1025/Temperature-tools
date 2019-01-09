# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 10:16:32 2018

@author: chaos
"""
import csv
import ast
import argparse
from func_fit import funz_rev, load_data_temperature

def parse_args_fix(check=True):
	## argparse does NOT type bool. Use ast.literal_evaal instead.
    parser = argparse.ArgumentParser(description='A procedure to estimate the coefficients of the temperature curvs')
    
    parser.add_argument("--output_file_name", type=str, default="fix_output.csv",
                        help="The list of the output data file in csv format, seperated by ;")
    parser.add_argument("--list_csv_data_files", type=str, default=None,
                        help="The list of the input data files in csv format, seperated by .")
    parser.add_argument("--b_handle_as_one", type=ast.literal_eval, default=True,
                        help="Should we merge all the input data to fit a singe curve.")
    parser.add_argument("--model_types", type=str, default='pow', 
                        help="The fitting fuction for the given data. Options are: poly, pow, exp. This arguments can be a list seperated by comma.")
    parser.add_argument("--col_black", type=int, default=2,
                        help="The index of colume of value x in the data file.")
    parser.add_argument("--col_record", type=int, default=0,
                        help="The index of colume of value y in the data file.")
    parser.add_argument("--splitchar", type=str, default=';',
                        help="The index of colume of value y in the data file.")
    parser.add_argument("--rescale_factor", type=float, default=100.0,
                        help="The rescale factor for x in the data file.")
    parser.add_argument("--coeffs_a", type=float, default=None,
                        help="The rescale factor for x in the data file.")
    parser.add_argument("--coeffs_b", type=float, default=None, 
                        help="The rescale factor for x in the data file.")
    parser.add_argument("--coeffs_c", type=float, default=None, 
                        help="The rescale factor for x in the data file.")
    
    FLAGS, unparsed = parser.parse_known_args()
    
    return FLAGS, unparsed

def save_data_in_csv_format(filename, data_x, data_y):
    with open(filename,'w+', newline='') as myFile:
        writer =csv.writer(myFile)
        for idx in range(len(data_x)):
            row = [data_x[idx], data_y[idx]]
            writer.writerow(row)

def main():
    FLAGS, unparsed = parse_args_fix()
    
    if not FLAGS.list_csv_data_files:
        raise ValueError("You must give some data.")
    
    csv_file_name  = FLAGS.output_file_name; print(csv_file_name)
    lst_csv_input  = FLAGS.list_csv_data_files; print(lst_csv_input)
    b_input_merge  = FLAGS.b_handle_as_one; print(b_input_merge)
    lst_model_type = FLAGS.model_types
    
    splitchar = FLAGS.splitchar
    col_x     = FLAGS.col_black  # The value set on the block box.
    col_y     = FLAGS.col_record # The values manually record.
    rescale_f = FLAGS.rescale_factor
    ## Coefficients
    coeffs_a = FLAGS.coeffs_a
    coeffs_b = FLAGS.coeffs_b
    coeffs_c = FLAGS.coeffs_c
    
     # Check if the number of parameter of the lst_csv_input and ls_model_type equal
    lst_input_path  = lst_csv_input.split(',')
    lst_input_mtype = lst_model_type.split(',')
    
    if (True == b_input_merge) & (1 != len(lst_input_mtype)):
        raise ValueError('The type of target model must be 1 if you take all data into one model')
    elif (False == b_input_merge) & (len(lst_input_path) != len(lst_input_mtype)):
        raise ValueError('The number of the target model types must be equal to the number of input data files if you want to fit different models')
    
    x_v, y_v = [], []
    for filename in lst_input_path:
        x, y, _ = load_data_temperature(filename, splitchar, col_x, col_y, rescale_f)
        if True == b_input_merge:
            x_v.extend(x)
            y_v.extend(y)
        else:
            x_v.append(x)
            y_v.append(y)
    
    # Fit funcs   
    range_max = 1 if b_input_merge else len(x_v)
    # range_max = b_input_merge and 1 or len(x_v)
    for idx in range(range_max):
        func_type = lst_input_mtype[idx]
        print(func_type)
        if b_input_merge:
        	x = x_v
        	y = y_v
        else:
        	x = x_v[idx]
        	y = y_v[idx]
        # Reverse and save.
        fix_y = []
        for y_ in y:
            fix_r_ = funz_rev(y_, coeffs_a, coeffs_b, coeffs_c) 
            # print(y_)
            # print(fix_r_)
            fix_y.append(fix_r_);
        
        # Save as csv format.
        save_data_in_csv_format(csv_file_name, x, fix_y)
    
if __name__ == '__main__':
    '''
    Note: You must convert the Excel file into csv format before calling this script.
    Usage:
    python func_fit_rev_fix.py \
        --output_file_name=fix_output.csv \
        --list_csv_data_files=blackpanel.csv,camera2.csv \
        --b_handle_as_one=False \
        --model_types=pow,poly \
        --col_black=2 \
        --col_record=0 \
        --splitchar=';' \
        --rescale_factor=100.0 \
        --coeffs_a=78.9 \
        --coeffs_b=0.2345 \
        --coeffs_c=-778.9
    
    For short, it can be:
    python func_fit_rev_fix.py \
        --output_file_name=fix_output.csv \
        --list_csv_data_files=blackpanel.csv,camera2.csv \
        --b_handle_as_one=True \
        --model_types=pow \
        --rescale_factor=100.0 \
        --coeffs_a=78.9 \
        --coeffs_b=0.2345 \
        --coeffs_c=-778.9
    '''
    main()
