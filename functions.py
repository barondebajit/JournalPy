import os
import json
import pyfiglet
from transformers import pipeline
from colorama import Fore, Style

def configcreate(filename):
    print(Fore.LIGHTCYAN_EX,"Enter your name: ",end = "")
    print(Style.RESET_ALL,end = "")
    username = input()
    print("")

    print(Fore.LIGHTCYAN_EX,"Enter the app name (default: JournalPy): ",end = "")
    print(Style.RESET_ALL,end = "")
    appname = input()
    if appname == "":
        appname = "JournalPy"
    print("")


    print(Fore.LIGHTCYAN_EX,"Enter 1 for using date format [DD/MM/YYYY].")
    print(Fore.LIGHTCYAN_EX,"Enter 2 for using date format [MM/DD/YYYY].")
    print(Fore.LIGHTCYAN_EX,"Enter your choice: ",end = "")
    print(Style.RESET_ALL,end = "")
    dateformat = input()
    print("")

    data = {
        "appname" : appname,
        "user" : username,
        "dateformat" : dateformat
    }

    with open(filename,"w") as cfg:
        json.dump(data,cfg,indent = 4)
    
    clear()

def getgreeting(now):
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 16:
        greeting = "Good Afternoon"
    elif 16 <= hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"
    return greeting

def welcome(appname,greeting,username,date,time):
    pyfiglet.print_figlet("{}".format(appname),"standard","green")
    print(Fore.LIGHTCYAN_EX,"{}, {}.".format(greeting,username))
    print(Fore.LIGHTMAGENTA_EX,"Today is {}.".format(date))
    print(Fore.LIGHTYELLOW_EX,"Time: {} hrs.".format(time))
    print(Style.RESET_ALL)

def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def help():
    print(Fore.LIGHTCYAN_EX,"Available Commands-")
    print(Fore.LIGHTMAGENTA_EX,"    help")
    print(Fore.LIGHTYELLOW_EX,"         -Display Information")
    print(Fore.LIGHTMAGENTA_EX,"    write")
    print(Fore.LIGHTYELLOW_EX,"         -Start journaling")
    print(Fore.LIGHTMAGENTA_EX,"    show")
    print(Fore.LIGHTYELLOW_EX,"         -View past journals")
    print(Fore.LIGHTMAGENTA_EX,"    chat")
    print(Fore.LIGHTYELLOW_EX,"         -Chat with me")
    print(Fore.LIGHTMAGENTA_EX,"    refresh")
    print(Fore.LIGHTYELLOW_EX,"         -Refresh the screen")
    print(Fore.LIGHTMAGENTA_EX,"    exit")
    print(Fore.LIGHTYELLOW_EX,"         -Close the program")
    print(Style.RESET_ALL)

def write(username,date):
    date = date.replace(" ","_")
    date = date.replace(",","")
    print(Fore.LIGHTCYAN_EX,"Hey there {}. How do you feel?".format(username))
    print(Fore.LIGHTCYAN_EX,"> ",end = "")
    print(Style.RESET_ALL,end = "")
    feelings = input()
    print("")

    print(Fore.LIGHTCYAN_EX,"How many goals do you want to set today?")
    print(Fore.LIGHTCYAN_EX,"> ",end = "")
    print(Style.RESET_ALL,end = "")
    goalcount = int(input())

    goal = []
    for i in range(goalcount):
        print(Fore.LIGHTCYAN_EX,"Enter goal {}: ".format(i+1),end = "")
        print(Style.RESET_ALL,end = "")
        goal.append(input())
    
    print(Fore.LIGHTGREEN_EX,"Saving journal.")
    with open("Journal_{}.txt".format(date),"a") as file:
        file.write("Feelings:\n")
        file.write(feelings+"\n\n")
        file.write("Goals:\n")
        for i in range(goalcount):
            file.write(goal[i]+"\n")
    print(Fore.LIGHTGREEN_EX,"Journal saved. Thank You for writing.")
    print(Style.RESET_ALL)

def show(dateformat):
    datedict = {
        "01" : "January",
        "02" : "February",
        "03" : "March",
        "04" : "April",
        "05" : "May",
        "06" : "June",
        "07" : "July",
        "08" : "August",
        "09" : "September",
        "10" : "October",
        "11" : "November",
        "12" : "December"
    }
    print(Fore.LIGHTCYAN_EX,"Enter the date whose journal entry you want to see in {} format: ".format("DD/MM/YYYY" if dateformat == "1" else "MM/DD/YYYY"),end = "")
    print(Style.RESET_ALL,end = "")
    date = input()
    datelist = date.split("/")
    if dateformat == "1":
        day = datelist[0]
        month = datedict[datelist[1]]
        year = datelist[2]
    else:
        day = datelist[1]
        month = datedict[datelist[0]]
        year = datelist[2]
    
    try:
        with open("Journal_{}_{}_{}.txt".format(day,month,year),"r") as file:
            content = file.read()
            print(Fore.LIGHTBLUE_EX,content)
            print(Style.RESET_ALL)
    except:
        print(Fore.LIGHTRED_EX,"No journal entry found for {}".format(date))
        print(Style.RESET_ALL)

def chat(appname,username):
    chatbot = pipeline('text2text-generation', model='facebook/blenderbot-400M-distill')
    chat_history = []
    chat_history.append({'generated_text': "Hello {}. I am {}. How may I help you?".format(username,appname), 'user_input': None})

    print(Fore.LIGHTCYAN_EX,"{}> {}".format(appname,chat_history[-1]['generated_text']))
    print(Style.RESET_ALL,end = "")
    while True:
        print(Fore.LIGHTBLUE_EX,"{}> ".format(username),end = "")
        print(Style.RESET_ALL,end = "")
        user_input = input()
        if user_input.lower() in ['exit', 'quit']:
            break

        response = chatbot(user_input)
        chat_history.append({'generated_text': response[0]['generated_text'], 'user_input': user_input})

        print(Fore.LIGHTCYAN_EX,"{}>{}".format(appname,response[0]['generated_text'].lstrip(" ")))
        print(Style.RESET_ALL,end = "")