#!/usr/bin/python3
# -*- coding: utf-8 -*-
## ch.py --- Un shell pour les hélvètes.
import os
import sys
from shutil import copyfile

def main():
    while True:
        sys.stdout.write("%% ")
        line = input()
        dirs = os.listdir()
        d = " ".join(dirs)
        new_line = ""
        for char in line:
            if char == "*":
                new_line += d
            else:
                new_line += char
        args = list(filter(None, new_line.split(" ")))
        list_arg = []
        src = None
        dst = None
        cmd = args[0]
        data = iter(args)
        for temp in data:
            if temp == "<":
                src = next(data)
            elif temp[0] == "<":
                src = temp[1:]
            elif temp == ">":
                dst = next(data)
            elif temp[0] == ">":
                dst = temp[1:]
            else:
                list_arg.append(temp)    
        if dst:
            output = os.open(dst, os.O_CREAT |os.O_WRONLY |os.O_TRUNC)
        else:
            output = 0
        if src:
            if os.path.exists(src):
                input_ = os.open(src, os.O_RDONLY)
            else:
                sys.stdout.write("Bash: "+src+" :No such file or directory \n")
                continue
        else:
            input_ = 1
        if cmd=="exit":
            break
        try:
            pid = os.fork() 
            if pid == 0:
                os.dup2(input_,0)
                os.dup2(output,1) 
                os.execvp(cmd,list_arg)
            else:
                os.waitpid(pid,0)
        except:
            sys.stdout.write("Ops: "+cmd+" :command not found\n")
    sys.stdout.write("Bye!\n")
    sys.exit(0)

main()