#!/usr/bin/env python3 
import pyperclip as pycp
import os 
import re 
import time

sayntax = "[a-zA-Z0-9]+\:[1-9]+[0-9]*?$"
TemplatPath = '/opt/tools/PayClip/templates/' 
InintText = os.popen('xclip -o ').read().strip()

# InintText = input(" just testing if its working : ")
if re.search(sayntax,InintText): 
    Plist = InintText.split(':')
    filename = Plist[0]
    pyindex = int(Plist[1])
    
    try : 
        FilePayload = open(TemplatPath+filename,'r')
        threshold = 1 
        NotFound = True 
        for Payload in FilePayload.readlines() : 
            if Payload[0] == '#' or Payload.strip() == '' :
                continue
            
            if threshold == pyindex : 
                
                os.system(f"echo '{Payload.strip()}' | xclip -selection clipboard")
                time.sleep(0.50)
                os.system('xdotool  key ctrl+V')
                # print(Payload.strip())
                NotFound = False 
                break
            threshold +=1 
        if NotFound : 
            os.system("notify-send 'The payload row is less then "+str(pyindex)+"'")

    except : 
        os.system("notify-send 'there is error on the template folder plz see if the file exist'")
else : 
    os.system("notify-send 'errer santax'")