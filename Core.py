"""
    Rachel's Core

    Written by -> Amirhossein Mohammadi & Erfan Saberi
    github.com/BlackIQ
    github.com/erfansaberi

    Rachel's Version -> 0.0.1
    Core's  Version  -> 0.0.1
"""

# Import System Libs
import os
# Import Net Libs
import webbrowser
import googlesearch
# Import Date and Time Libs
from time import *
# Import Text Libs
import random

from var.Data import *

# Functions
def start():
    start_list = [
        f'Welcome back {UserName} !',
        f'Hi {UserName} !',
        f'Hello {UserName} ! I missed U :)'
        f'Hi Honey !'
    ]
    print(random.choice(start_list))
    print(f'Today is : (', strftime("%Y , %m , %d" , localtime()), f') {UserName}')

def clear() :
    os.system("clear")

def hello():
    hello_list = [
        f'Hello {UserName} !',
        'Hi Darline !',
        'Hello my love !' ,
        f'Welcome Back {UserName} .'
    ]
    print(random.choice(hello_list))

def bye():
    bye_list = [
        'bye sweetie .' ,
        f'Bye {UserName}'
    ]
    print(random.choice(bye_list))

def Goodnight():
    print(f'Have a Good night {UserName} .')
    print('I hope you sleep well !')

def Sleep():
    print('Oh , OK !')
    print('Goodbye Pal !')

def problem():
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
        print(f'Today is : (', n_date, ') {UserName}')
    if 'i' in ask_date:
        i_date = strftime("%Y , %m , %d" , localtime())
        print(f'Today is : (', i_date, ') {UserName}')

def Time():
    ask_time = input('[gmt] or [i]ran ? ')

    if 'gmt' in ask_time:
        gmt = strftime("%H : %M : %S", gmtime())
        print(f'Now is : (', gmt, ') {UserName}')
    if 'i' in ask_time:
        i_time = strftime("%Y , %m , %d" , localtime())
        print('Now is : (', i_time, f') {UserName}')

def search_in_net(text):
    results = googlesearch.search(text)
    i = 0
    for result in results:
        print(f"[{i}]" + result)
        i += 1
    num = input('\n[?] Insert number to open url in browser : ')
    if num:
        webbrowser.open(results[int(num)])
    return ''