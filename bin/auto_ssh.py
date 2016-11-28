#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys, base64

def choose():
    of = open("./data/information.d")
    hosts = of.readlines()
    while 1:
        print("=================SSH===================")
        print("+{}+".format("-"*35))
        print("|     UserName    IP:PORT")
        l = len(hosts)
        for i in range(0, l):
            v_list = hosts[i].split(" ")
            print("+{}+".format("-"*35))
            print("| {} | {} {}:{}".format(i+1, v_list[0], v_list[1], v_list[2]))
        print("+{}+".format("-"*35))
        c = raw_input("[SSH]Choose the number or name('#q' exit):")
        is_name = False
        is_y = False
        try:
            c = int(c)
            if c > l or c < 1:
                print("[Warning]:There is no")
                continue
            l_list = hosts[c-1].split(" ")
            name = l_list[0]
            host = l_list[1]
            port = l_list[2]
            password = l_list[3]
            is_y = True
            
        except:
            is_name = True
        if is_name:
            if c.strip() == "#q":
                return
            for l in hosts:
                if c.strip() == l.split(" ")[0].strip():
                    l_list = l.split(" ")
                    name = l_list[0]
                    host = l_list[1]
                    port = l_list[2]
                    password = l_list[3]
                    is_y = True
                    
        if not is_y:
            continue

        # ssh
        password = base64.decodestring(password)

        print("In the connection...")
        if port == "22":
            connection("ssh {}@{}".format(name, host), password)
           
        else:
            connection("ssh {}@{}:{}".format(name, host, port), password)
  
def connection(cmd, pwd):
    import pexpect
    child = pexpect.spawn(cmd)
    i = child.expect([".*password.*",pexpect.EOF, pexpect.TIMEOUT])
    if( i == 0 ):
        child.sendline("{}\n".format(pwd))
        child.interact()
        
    else:
        print("[Error]The connection fails")

