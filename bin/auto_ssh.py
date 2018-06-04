#-*-coding:utf-8-*-
import os, sys, base64
__author__ = 'Allen Woo'
path = os.path.dirname(os.path.abspath(sys.argv[0]))

def choose():
    
    of = open("{}/data/information.d".format(path))
    hosts = of.readlines()
    hosts_temp = []
    for h in hosts:
        if h.strip():
            hosts_temp.append(h)
    hosts = hosts_temp[:]
    l = len(hosts)
    if l <= 0:
        os.system("clear")
        print("[Warning]Please add the host server")
        return

    password = ""
    while 1:
        
        print("=================SSH===================")
        print("+{}+".format("-"*40))
        print("|     Alias   UserName@IP:PORT")
        print("+{}+".format("-"*40))
        for i in range(0, l):
            v_list = hosts[i].strip().split(" ")
            print(" {} | {}   {}@{}:{}".format(i+1, v_list[4], v_list[0], v_list[1], v_list[2]))
        print("+{}+".format("-"*40))
        c = input("[SSH]Choose the number or alias('#q' exit):")
        is_alias = False
        is_y = False
        try:
            c = int(c)
            if c > l or c < 1:
                os.system("clear")
                print("[Warning]:There is no")
                continue
            l_list = hosts[c-1].strip("\n").split(" ")
            name = l_list[0]
            host = l_list[1]
            port = l_list[2]
            password = l_list[3]
            is_y = True
            
        except:
            is_alias = True
        if is_alias:
            if c.strip() == "#q":
                os.system("clear")
                return
            for h in hosts:
                if c.strip() == h.split(" ")[4].strip():
                    l_list = h.split(" ")
                    name = l_list[0]
                    host = l_list[1]
                    port = l_list[2]
                    password = l_list[3]
                    is_y = True
                    
        if not is_y:
            continue


        # ssh
        password = base64.decodebytes(password.encode("utf-8")).decode("utf-8")
        print("In the connection...")
        print("{}@{}".format(name, host))
        if port == "22":
            connection("ssh {}@{}".format(name, host), password)
           
        else:
            connection("ssh {}@{} -p {}".format(name, host, port), password)
  
def connection(cmd, pwd):
    import pexpect
    child = pexpect.spawn(cmd, maxread=10000)
    i = child.expect([".*password.*", ".*continue.*?", pexpect.EOF, pexpect.TIMEOUT])
    if( i == 0 ):
        child.sendline("{}\n".format(pwd))
        child.interact()
    elif( i == 1):
        child.sendline("yes\n")
        child.sendline("{}\n".format(pwd))
        
        #child.interact()    
    else:
        print("[Error]The connection fails")

