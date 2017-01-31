#!/usr/bin/python3
# -*- coding: utf-8 -*-
## ch.py --- Un shell pour les hélvètes.
import os
import sys
def main():
    while True:
        sys.stdout.write("$")
        line = input()
        if len(line)==0:   #Si on tape rien, on continue la boucle de while
            continue
        dirs = os.listdir()
        d = " ".join(dirs)
        new_line = ""
        for char in line:
            if char == "*":
                new_line += d
            else:
                new_line += char
        args = list(filter(None, new_line.split(" "))) #Pour eliminer les espaces.
        cmd = args[0]
        if cmd=="exit":
            break
            sys.exit(0)
        pid=True
        list_arg = []
        src = None
        dst = None
        output=1
        input_=0
        data = iter(args)  #iterateur sert a construire list_arg ou il n'y a pas les signes de redirection.
        for temp in data:
            if temp == "<":  #Si on trouve le signe de stdin, le fichier source sera l'element suivant
                src = next(data)
            elif temp[0] == "<": #Sinon, si le signe de stdin est collé avec le nom du fichier, on le separe..
                src = temp[1:]
            elif temp == ">":      #Meme chose comme avec "<"
                dst = next(data) 
            elif temp[0] == ">":
                dst = temp[1:]
            else:
                list_arg.append(temp) #Construction de liste d'arguemnts sans les signes de redirection
        list_arg=list_arg[1:] # pour eliminer le cmd du list, sinon ca fait un bug avec les pipes.   
        if dst:                                             #Si il y'a fichier dest, on le cree. J'ai pas pris en compte le >> ou &2>
            output = os.open(dst, os.O_CREAT |os.O_WRONLY) 
        if src:                                             #Si on detecte un fichier source, on l'ouvre READ ONLY, sinon on affiche erreur.
            if os.path.exists(src):             
                input_ = os.open(src, os.O_RDONLY) 
            else:
                sys.stdout.write("Bash: "+src+" :No such file or directory \n") #Error
                continue
        while '|' in list_arg:  
            for i in range(len(list_arg)):
                if list_arg[i] == '|':
                    r, w = os.pipe()     #file descriptors
                    pid = os.fork()                   
                    if pid:         #Pour le parent
                        os.close(w)        
                        input_ = r   
                        cmd = list_arg[i + 1]   # Prendre la commande apres le pipe
                        list_arg = list_arg[i + 2:]  #Construire la liste de la commande du parent
                        break             
                    else:           #Pour le child
                        os.close(r)    
                        output = w  
                        list_arg = list_arg[:i]    #Arguments de la commande du child
                        break
        try:
            if pid:          
                pid = os.fork() 
            if pid == 0:
                os.dup2(output,1)
                os.dup2(input_,0) 
                os.execvp(cmd,[cmd]+list_arg)
            else:
                os.waitpid(pid,0)
        except:
            sys.stdout.write("Ops: "+cmd+" :command not found\n")
    sys.stdout.flush()
    sys.stdout.write("Bye!\n")
    sys.exit(0)
main()
