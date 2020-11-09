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

from libra.data import *

# Functions

class dt() :
    def Date(self):
        ask_date = input('[n]ational Or [i]ran ? ')

        if 'n' in ask_date:
            n_date = strftime("%Y-%m-%d", localtime())
            print(f'Today is : (', n_date, ') {UserName}')
        if 'i' in ask_date:
            i_date = strftime("%Y , %m , %d", localtime())
            print(f'Today is : (', i_date, ') {UserName}')

    def Time(self):
        ask_time = input('[gmt] or [i]ran ? ')

        if 'gmt' in ask_time:
            gmt = strftime("%H : %M : %S", gmtime())
            print(f'Now is : (', gmt, ') {UserName}')
        if 'i' in ask_time:
            i_time = strftime("%Y , %m , %d", localtime())
            print('Now is : (', i_time, f') {UserName}')


class app() :
    def uninstall(self):
        print("Are you sure for uninstalling ?")
        a = input("[Y]es , [n]o : ")
        if a == "Y":
            print("I ask one more time !")
            aa = input("[Y]es , [n]o : ")
            if aa == "Y":
                os.system('sudo rm -rf /home/amir/Rachel/ /usr/bin/Rachel && exit')
            else:
                print('Wow !')
        else:
            print("Wow !")

    def version(self) :
        print('Rachel is on 0.0.3 !')

class Hi() :
    def start(self):
        start_list = [
            f'Welcome back {UserName} !',
            f'Hi {UserName} !',
            f'Hello {UserName} ! I missed U :)'
            f'Hi Honey !'
        ]
        print(random.choice(start_list))
        print(f'Today is : (', strftime("%Y , %m , %d", localtime()), f') {UserName}')

    def hello(self):
        hello_list = [
            f'Hello {UserName} !',
            'Hi Darline !',
            'Hello my love !',
            f'Welcome Back {UserName} .'
        ]
        print(random.choice(hello_list))

class Bye() :
    def bye(self):
        bye_list = [
            'bye sweetie .',
            f'Bye {UserName}'
        ]
        print(random.choice(bye_list))

    def Goodnight(self):
        print(f'Have a Good night {UserName} .')
        print('I hope you sleep well !')

    def Sleep(self):
        print('Oh , OK !')
        print('Goodbye Pal !')

def clear() :
    os.system("clear")

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