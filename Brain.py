import datetime
import random
from math import *
from time import *
import requests
from jdatetime import *
from config import username
import webbrowser
import googlesearch
import os
from difflib import get_close_matches

# Functions
def start():
    start_list = [f'Welcome back {username} !',
                  f'Hi {username} !', f'Hello {username} ! I missed U :)']
    print(random.choice(start_list))
    print(f'Today is : (', datetime.now().date().strftime(
        "%Y , %m , %d"), f') {username}')

def clear() :
    os.system("clear")

def hello():
    hello_list = [f'Hello {username} !', 'Hi Darline !', 'Hello my love !']
    print(random.choice(hello_list))


def bye():
    print(f'Goodbye {username} !')


def Goodnight():
    print(f'Have a Good night {username} .')
    print('I hope you sleep well !')


def Sleep():
    print('Oh , OK !')
    print('Goodbye Pal !')


def problem():
    print('Oh sorry , Some thing went wrog :-(')
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


# def chat(text):
#     if text in chatDict:
#         return chatDict[text]
#     elif len(get_close_matches(text, chatDict.keys())) > 0:
#         closest_match = get_close_matches(text, chatDict)[0]
#         response = chatDict[closest_match]
#         if type(response) == str:
#             return response
#         elif type(response) == list:
#             return response[random.randint(0, len(response)-1)]
#     else:
#         return ''


def search_in_net(text):
    results = googlesearch.search(text)
    i = 0
    for result in results:
        print(f"[{i}]" + result)
        i += 1
    num = input('\n[?] Insert number to open url in browser: ')
    if num:
        webbrowser.open(results[int(num)])
    return ''
