#!/usr/bin/env python3
# -*- utf:8; -*-
'''
**代理工具
**2019.01.08
**by King-1025
'''
import sys
import os

requirements=sys.path[0]+os.sep+"requirements.txt"

# fix windows10 bug 2020.6.19
handler_xlsx2csv="python "+sys.path[0]+os.sep+"xls-2csv.py"+" "
handler_csv2data="python "+sys.path[0]+os.sep+"csv2data.py"+" "

def solve_requirements():
      os.system("pip install -r "+str(requirements))
      print("\nall requirements ok!")

def remove_requirements():
      os.system("pip uninstall -r "+str(requirements))

def help(s):
      print("Usage: %s sub-command\n" % s)
      print("Example:%s -l output 1.xlsx" % s)
      print("\t%s csv 1.xlsx" % s)
      print("\t%s data 1.csv" % s)
      print("\t%s help" % s)

if __name__ == "__main__":
    sys.argc=len(sys.argv)
    if sys.argc == 1:
        print("support:csv,data,cat,ok,bye,help")
    else:
        index,ch=1," "
        sub=sys.argv[index]
        command=None
        if sub == "csv":
            command=str(handler_xlsx2csv)
        elif sub == "data":
            command=str(handler_csv2data)
        elif sub == "ok":
            solve_requirements()
        elif sub == "cat":
            print("此命令暂未实现！")
        elif sub == "bye":
            remove_requirements()
        elif sub == "help":
            help(os.path.basename(sys.argv[0]))
        else:
            print("unknown sub-command:%s" % sub)
        if command != None:
            index+=1
            for i in range(index,sys.argc):
                if i != index:
                   command+=ch
                command+=str(sys.argv[i])
            print(command)
            os.system(command)
            
            
