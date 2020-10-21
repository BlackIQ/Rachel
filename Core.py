# Import Owns
from config import username

# Import System Libs
import os

# Import Net Libs
import webbrowser
import googlesearch
import requests
import bs4

# Import Date and Time Libs
import datetime
from time import *
from jdatetime import *

# Import Text Libs
from difflib import get_close_matches
import random

# Import Speech Libs
import pyttsx3

# Import App Libs
from playsound import playsound

engine = pyttsx3.init()

# Functions
def start():
    engine. setProperty("rate", 150)
    engine.say("Hi .")
    sleep(1)
    engine.say("I am Rachel !")
    engine.runAndWait()
    # start_list = [f'Welcome back {username} !',
    #               f'Hi {username} !', f'Hello {username} ! I missed U :)']
    # print(random.choice(start_list))
    # print(f'Today is : (', datetime.now().date().strftime(
    #     "%Y , %m , %d"), f') {username}')

def Music() :
    engine.say("Ok , give me the address .")
    engine.runAndWait()
    print("Ok , give me the address .")
    engine.say("Address : ")
    engine.runAndWait()
    address = input("Address : ")
    playsound(address) 

def clear() :
    os.system("clear")

def hello():
    hello_list = [f'Hello {username} !', 'Hi Darline !', 'Hello my love !']
    print(random.choice(hello_list))

def bye():
    engine.say("GoodBye .")
    engine.runAndWait()
    print(f'Goodbye {username} !')

def Goodnight():
    engine.say("Have a good night .")
    engine.say("I Hope you sleep well .")
    engine.runAndWait()
    print(f'Have a Good night {username} .')
    print('I hope you sleep well !')

def Sleep():
    engine.say("Oh , Ok !")
    engine.say("Goodbye pal !")
    engine.runAndWait()
    print('Oh , OK !')
    print('Goodbye Pal !')

def problem():
    engine.say("Oh sorry , Some thing went wrong .")
    engine.say("Please try again !")
    engine.runAndWait()
    print('Oh sorry , Some thing went wrong :-(')
    print('Please try again !')

def StarDate():
    YY = int(strftime("%Y", localtime())) - 1900
    MM = strftime("%m", localtime())
    DD = strftime("%d", localtime())
    print("Rachels Log , Stardate (", YY, MM, ".", DD, ") !")

def Date():
    ask_date = input('[s]tardate Or [n]ational Or [i]ran ? ')

    if 's' in ask_date:
        StarDate()
    if 'n' in ask_date:
        n_date = strftime("%Y-%m-%d", localtime())
        print(f'Today is : (', n_date, ') {username}')
    if 'i' in ask_date:
        i_date = datetime.now().date().strftime("%Y , %m , %d")
        print(f'Today is : (', i_date, ') {username}')

def Time():
    ask_time = input('[gmt] or [i]ran ? ')

    if 'gmt' in ask_time:
        gmt = strftime("%H : %M : %S", gmtime())
        print(f'Now is : (', gmt, ') {username}')
    if 'i' in ask_time:
        i_time = datetime.now().time().strftime("%H : %M : %S")
        print(f'Now is : (', i_time, ') {username}')

def search_in_net(text):
    results = googlesearch.search(text)
    i = 0
    for result in results:
        print(f"[{i}]" + result)
        i += 1
    engine.say("Insert number to open url in browser : ")
    engine.runAndWait()
    num = input('\n[?] Insert number to open url in browser : ')
    if num:
        webbrowser.open(results[int(num)])
    return ''