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
device_list={
   "160":{
           "func":sys.path[0]+os.sep+"func_fit_160.py",
           "type":{
                    "0":"pow"
           }
   },
   "320":{
           "func":sys.path[0]+os.sep+"func_fit_320.py",
           "type":{
                    "0":"pow",
                    "1":"poly"
           }
   }
}

def ask(msg):
    return tkinter.messagebox.askokcancel('提示', '要处理下一个吗？\n'+msg)

def command(func,model,inpath,outpath):
    stra=func+" --b_handle_as_one=False \
                --show_fitted_func=True \
                --splitchar=, \
                --rescale_factor=1.0 \
                --col_x=1 \
                --col_y=0"
    return stra+" --model_types="+model+" --list_csv_data_files="+inpath+" --binary_file_path="+outpath
   
csv_list=[]
def search(path,ext):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            search(item_path,ext)
        elif os.path.isfile(item_path):
            if os.path.splitext(item_path)[1] == ext:
                global csv_list
                csv_list.append(item_path)

def check_device(device,model):
    f,t=None,None
    if device not in device_list.keys():
       print("unknown device:"+device)
    else:
       f=device_list[device]["func"]
    if model != None:
       if model not in device_list[device]["type"].keys():
          print("unknown model:"+model)
       else:
          t=device_list[device]["type"][model]
    else:
       if device == "160":
          t="pow"
       elif device == "320":
          t="poly"
       else:
          print("device "+device+" hasn't default model value")
    return f,t

def check_outfile(model,outfile):
    #print(outfile)
    o=outfile
    if o == None:
      if model == "pow":
         o="powfitmap.data"
      elif model == "poly":
         o="powfitmap.data"
      else:
         o=model+".data"
    return o

def check_location(device,model,location):
    l=location
    if device == "160":
       l+=os.sep+device
    else: 
       l+=os.sep+device+os.sep+model
    return l

def convert(device,model,path,location="output",outfile="data.out"):
    f,t=check_device(device,model)
    print(f,t)
    if f == None or t == None:
       return
    for p in path:
         if os.path.exists(p):
             if os.path.isfile(p):
                 csv_list.append(p)
             elif os.path.isdir(p):
                 search(p,".csv")
    location=check_location(device,t,location)
    #print(device,location,outfile)
    i,count=1,len(csv_list)
    for csv in csv_list:
        lp=location+os.sep+os.path.basename(csv).split(".")[0]
        if not os.path.exists(lp):
            os.makedirs(lp)
        out=lp+os.sep+check_outfile(t,outfile)
        print("\n<====== %s\n" % csv)
        #print(command(f,t,csv,out))
        os.system(command(f,t,csv,out))
        print("\n======> %s" % out)
        if i < count:
           #if not ask("csv:"+csv_list[i]):
           if input("\n[%d] next csv file path:%s, continue ok? (yes/no)" %(count-i,csv_list[i])) == "no":
              break
           i+=1
    if count == 0:
       i=0
    print("\ncount:%d handle:%d location:%s" %(count,i,location))

def help(s=0):
    if s == 0:
       print("The tool can create bin-data by csv file.(%s)" % VERSION)
    print("Usage:%s <-d device> [-m model] [-l location] [-o outfile] <files|dirs>" % os.path.basename(sys.argv[0]))

if __name__ == "__main__":
    sys.argc=len(sys.argv)
    if sys.argc == 1:
        help()
    else:
        i,device,model,location,outfile,path=1,None,None,"output"+os.sep+"bin",None,[]
        while i < sys.argc:
            i,c=(i+1),sys.argv[i]
            if c == "-d":
                if i < sys.argc:
                    device=sys.argv[i]
                    i+=1
            elif c == "-m":
                if i < sys.argc:
                    model=sys.argv[i]
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
        print(device,model,location,outfile,path)
        if device != None and len(path) > 0:
           convert(device,model,path,location,outfile)
