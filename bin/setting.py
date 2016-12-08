#!/usr/bin/env python
#-*-coding:utf-8-*-
import re, base64, os, sys
path = os.path.dirname(os.path.abspath(sys.argv[0]))
'''
选项配置管理
__author__ = 'allen woo'
'''

def add_host_main():
    while 1:
        if add_host():
            break
        print("\n\nAgain:")

   
def add_host():
    
    print("================Add=====================")
    print("[Help]Input '#q' exit")
    host_ip = str_format("Host IP:", "^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
    if host_ip == "#q":
        return 1
    
    host_port = str_format("Host port(Default 22):", "[0-9]+")
    if host_port == "#q":
        return 1
    
    password = str_format("Password:", ".*")
    if password == "#q":
        return 1
    password = base64.encodestring(password)
    name = str_format("User Name:", "^[^ ]+$")
    if name == "#q":
        return 1
    elif not name:
        print("[Warning]:User name cannot be emptyg")
        return 0
    
    # The alias
    alias = str_format("Local Alias:", "^[^ ]+$")
    if alias == "#q":
        return 1
    elif not alias:
        print("[Warning]:Alias cannot be emptyg")
        return 0
        

    of = open("{}/data/information.d".format(path))
    hosts = of.readlines()
    for l in hosts:
        l = l.strip("\n")
        if not l:
            continue
        l_list = l.split(" ")
        if host_ip == l_list[1] and host_port == l_list[2]:
            print("[Warning]{}:{} existing".format(host_ip, host_port))
            return 0
        if alias == l_list[4]:
            print("[Warning]Alias '{}' existing".format(alias))
            return 0
    
    of.close()
    
    # save
    of = open("{}/data/information.d".format(path), "a")
    of.write("{} {} {} {} {}".format(name.strip("\n"), host_ip.strip("\n"), host_port, password.strip("\n"), alias.strip("\n")))
    of.close()
    return 1
    
def remove_host():
    while 1:
        
        of = open("{}/data/information.d".format(path))
        hosts = of.readlines()
        of.close
        l = len(hosts)
        if l <= 0:
            os.system("clear")
            print("[Warning]There is no host")
            return
            
        print("================Remove================")
        print("+{}+".format("-"*40))
        print("|     Alias   UserName@IP:PORT")
        for i in range(0, l):
            v_list = hosts[i].strip().split(" ")
            print("+{}+".format("-"*40))
            print("| {} | {}   {}@{}:{}".format(i+1, v_list[4], v_list[0], v_list[1], v_list[2]))
        print("+{}+".format("-"*40))
        c = raw_input("[Remove]Choose the Number or Alias('#q' to exit):")
        is_alias = False
        is_y = False
        try:
            c = int(c)
            if c > l or c < 1:
                os.system("clear")
                print("[Warning]:There is no")
                continue
            del hosts[c-1]
            is_y = True
            
        except:
            is_alias = True
        if is_alias:
            if c.strip() == "#q":
                os.system("clear")
                break
                
            n = 0
            for l in hosts:
                if c.strip() == l.split(" ")[4].strip():
                    del hosts[n]
                    is_y = True 
                n += 1
                   
                    
        if not is_y:
            os.system("clear")
            print("[Warning]:There is no")
            continue
        else:
            
            # save
            c = raw_input("Remove?[y/n]:")
            if c.strip().upper() == "Y":
                of = open("{}/data/information.d".format(path), "w")
                for l in hosts:
                    of.write(l)
                print("Remove the success！")
                of.close()


def str_format(lable, rule):
    while 1:
        print(lable)
        temp = raw_input().strip()
        m = re.match(r"{}".format(rule), temp)
        if m:
            break
        elif "port" in lable:
            temp = 22
            break
        elif temp.strip() == "#q":
            os.system("clear")
            break
        print("[Warning]:Invalid format")
    
    return temp

    
