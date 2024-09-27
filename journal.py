import os
import datetime
import json
import gradio as gr
from colorama import Fore, Back, Style
from functions import *

pwd = os.getcwd()
configdir = os.path.join(pwd,"config")
configfile = os.path.join(configdir,"config.json")

if os.path.isdir(configdir) == 0:
    os.makedirs(configdir)
    configcreate(configfile)
else:
    if os.path.isfile(configfile) == 0:
        configcreate(configfile)

with open(configfile,"r") as cfg:
    configdata = json.load(cfg)

appname = configdata["appname"]
username = configdata["user"]
terminate = False
dateformat = configdata["dateformat"]
now = datetime.datetime.now()
date = now.strftime("%d %B, %Y")
time = now.strftime("%H:%M")
greeting = getgreeting(now)

welcome(appname,greeting,username,date,time)

while terminate != True:
    print(Fore.LIGHTGREEN_EX,"{}> ".format(appname),end = "")
    print(Fore.LIGHTCYAN_EX,end = "")
    command = input()

    print(Style.RESET_ALL,end = "")
    if command in ["exit","quit"]:
        exit(0)
    elif command == "help":
        help()
    elif command == "refresh":
        clear()
        welcome(greeting,username,date,time)
    elif command == "write":
        write(username,date)
    elif command == "chat":
        chat(appname,username)
    elif command == "show":
        show(dateformat)