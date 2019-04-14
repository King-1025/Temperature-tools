#!/usr/bin/env python3
# -*- utf-8; -*-
'''
**转换xls/xlsx到csv文件 
**2019.01.06 
**by King-1025
'''
VERSION="pre-1.0"

import os
import csv
import re
import sys
import time as tim

try:
    import xlrd
except ImportError:
    print("\033[5;31mNot found xlrd! please use pip install xlrd\033[0m")
'''
try:
   import openpyxl
except ImportError:
   print("not found openpyxl! please use pip install openpyxl")
'''
#解析模式
modes={
      "origin":{
          "xlrd":0,
          "openpyxl":1
    }
}

def find_value(sheet,tag,X_offset=0,Y_offset=0):
    if sheet != None:
       if sheet.nrows != None and sheet.ncols != None:
           for i in range(0,sheet.nrows):
               for j in range(0,sheet.ncols):
                  if tag == sheet.cell_value(i,j):
                     x,y=i+Y_offset,j+X_offset
                     return x,y,sheet.cell_value(x,y)
    return None,None,None

def pick(sheet):
    _,_,who=find_value(sheet,"测试人：",1,0)
    _,_,time=find_value(sheet,"时间：",1,0)
    _,_,dev_code=find_value(sheet,"设备编号：",1,0)
    _,_,dev_id=find_value(sheet,"设备ID号：",1,0)
    start,_,_=find_value(sheet,"黑体温度",0,0)
    data=[[fix_header(value) for value in sheet.row_values(start)]]
    end=sheet.nrows-1
    while start<end:
       start+=1
       data.append(sheet.row_values(start))
    if dev_code == None:
       dev_code=str(tim.strftime("unknown_dev-code_%Y%m%d%H%M%S",tim.localtime(tim.time())))
    else:
       dev_code=int(dev_code)
    return str(who),str(time),str(dev_code),str(dev_id),data

def fix_header(s):
    if s == "黑体温度":
        return 25
    else:
        return re.sub("\D","",s)

def origin_xlrd_parse(path):
    print("called origin_xlrd_parse %s" % path)
    result=[]
    with xlrd.open_workbook(path) as wb:
     for sheet in wb.sheets():
       if wb.sheet_loaded(sheet.name):
          print("loaded sheet %s ok!" % sheet.name)
          who,time,dev_code,dev_id,data=pick(sheet)
          result.append({
                  "sheet_name":sheet.name,
                  "who":who,
                  "time":time,
                  "dev_code":dev_code,
                  "dev_id":dev_id,
                  "data":data
          })
    return result

def origin_openpyxl_parse(path):
    print("don't implement origin_openpyxl_parse")
    return None

def create_csv_file(data,prefix,location,outstyle):
    print("called create_csv_file")
    i=0
    for item in data:
       if outstyle == 0:
          name=item["dev_code"]+".csv"
       else:
          name=item["dev_code"]+"-"+item["time"]+".csv"
          if prefix != None:
            name=str(prefix)+"-"+name
          else:
            name=str(i)+"-"+name
       path=location+os.sep+name
       with open(path,'w', newline='') as f:
          if item["data"] != None:
             csv_write = csv.writer(f,dialect='excel')
             csv_write.writerows(item["data"])
             print("%d.sheet:%s -> %s" %(i,item["sheet_name"],path))
             i+=1

#代理函数，统一转换xls,xlsx文件
def convert(path,mode=0,prefix=None,location="output",outstyle=0):
    if os.path.exists(path) and os.path.isfile(path):
       data=None
       if mode == modes["origin"]["xlrd"]:
          data=origin_xlrd_parse(path)
       elif mode == modes["origin"]["openpyxl"]:
          data=origin_openpyxl_parse(path)
       else:
          print("unknown convert mode:%s" % mode)
       if data != None:
          lp=location+os.sep+os.path.basename(path).split(".")[0]
          if not os.path.exists(lp):
             os.makedirs(lp) 
          create_csv_file(data,prefix,lp,outstyle) 
       else:
          print("parse faild!")
    else:
        print("the script needs a valid xls/xlsx file path(%s)" % path)

def help(s=0):
    if s == 0:
      print("The tool can onvert xls/xlsx to csv file.(%s)" % VERSION)
    print("Usage:%s [-m mode] [-p prefix] [-l location] [-o outstyle] <path-list>" % os.path.basename(sys.argv[0]))

if __name__ == "__main__":
   sys.argc=len(sys.argv)
   if sys.argc == 1:
       help()
   else:
       i,mode,prefix,location,outstyle,path=1,0,None,"output"+os.sep+"csv",0,[]
       while i < sys.argc:
           i,c=(i+1),sys.argv[i]
           if c == "-m":
             if i < sys.argc:
                mode=int(sys.argv[i])
                i+=1
           elif c == "-p":
             if i < sys.argc:
                prefix=sys.argv[i]
                i+=1
           elif c == "-l":
             if i < sys.argc:
                location=sys.argv[i]
                i+=1
           elif c == "-o":
             if i < sys.argc:
                outstyle=int(sys.argv[i])
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
       for p in path:
         convert(p,mode,prefix,location,outstyle)
       #print(i,mode,prefix,location,outstyle,path)
