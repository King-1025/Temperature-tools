#!/usr/bin/env python3
# -*- utf:8; -*-
'''
**处理csv文件 
**2019.01.08
**by King-1025
'''

VERSION="pre-1.1"

import sys
import os
import re

try:
   import tkinter
   import tkinter.messagebox
except ImportError:
   print("\033[5;31mNot found tkinter! please use pip install tkinter\033[0m")

#from func_fit import main as data

#设备类型
types={
   "160":"pow",
   "320":"poly"
}

def ask(msg):
    return tkinter.messagebox.askokcancel('提示', '要处理下一个吗？\n'+msg)

def command(model,inpath,outpath):
    stra=sys.path[0]+os.sep+"func_fit.py \
           --b_handle_as_one=False \
           --show_fitted_func=True \
           --splitchar=, \
           --rescale_factor=1.0 \
           --col_x=1 \
           --col_y=0"
    return stra+" --model_types="+model+" --list_csv_data_files="+inpath+" --binary_file_path="+outpath
                             
csv_list=[]
def search(path,pattern):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search(item_path,pattern)
        elif os.path.isfile(item_path):
            #if re.match(pattern,item_path) != None:
            if pattern in item_path:
                global csv_list
                csv_list.append(item_path)

def convert(device,path,location="output",outfile="data.out"):
    if device not in types.keys():
       print("unknown device:"+device)
       return
    for p in path:
         if os.path.exists(p):
             if os.path.isfile(p):
                 csv_list.append(p)
             elif os.path.isdir(p):
                 search(p,"csv")
    location+=os.sep+device
    #print(device,location,outfile)
    i,count=1,len(csv_list)
    for csv in csv_list:
        lp=location+os.sep+os.path.basename(csv).split(".")[0]
        if not os.path.exists(lp):
            os.makedirs(lp)
        out=lp+os.sep+outfile
        print("\n<====== %s\n" % csv)
        #print(command(types[device],csv,out))
        os.system(command(types[device],csv,out))
        print("\n======> %s" % out)
        if i < count:
           if not ask("csv:"+csv_list[i]):
               break
           i+=1
    print("\ncount:%d handle:%d location:%s" %(count,i,location))

def help(s=0):
    if s == 0:
       print("The tool can create bin-data by csv file.(%s)" % VERSION)
    print("Usage:%s <-d device> [-l location] [-o outfile] <files|dirs>" % os.path.basename(sys.argv[0]))

if __name__ == "__main__":
    sys.argc=len(sys.argv)
    if sys.argc == 1:
        help()
    else:
        i,device,location,outfile,path=1,None,"output"+os.sep+"bin","powfitmap.data",[]
        while i < sys.argc:
            i,c=(i+1),sys.argv[i]
            if c == "-d":
                if i < sys.argc:
                    device=sys.argv[i]
                    i+=1
            elif c == "-l":
                if i < sys.argc:
                    location=sys.argv[i]
                    i+=1
            elif c == "-o":
                if i < sys.argc:
                    outfile=sys.argv[i]
                    i+=1
            elif c == "-v":
                print(VERSION)
                exit()
            elif c == "-h":
                  help(1)
                  exit()
            else:
                path=sys.argv[(i-1):]
                break
        print(device,location,outfile,path)
        if device != None and len(path) > 0:
           convert(device,path,location,outfile)
