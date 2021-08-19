"""
    Rachel's Core

    Written by -> Amirhossein Mohammadi & Erfan Saberi
    github.com/BlackIQ
    github.com/erfansaberi

    Rachel's Version -> 0.0.1
    Core's  Version  -> 0.0.1
"""

import gtts
import os
import webbrowser
import googlesearch
from time import *
import random

from libra.data import *


# Classes

class dt:
    """
        Date and Time class
        It this class there are date methods, time methods
    """

    @staticmethod
    def Date():
        ask_date = input('[n]ational Or [i]ran ? ')

        if 'n' in ask_date:
            n_date = strftime("%Y-%m-%d", localtime())
            print(f'Today is : (', n_date, ') {UserName}')
        if 'i' in ask_date:
            i_date = strftime("%Y , %m , %d", localtime())
            print(f'Today is : (', i_date, ') {UserName}')

    @staticmethod
    def Time():
        ask_time = input('[gmt] or [i]ran ? ')

        if 'gmt' in ask_time:
            gmt = strftime("%H : %M : %S", gmtime())
            print(f'Now is : (', gmt, ') {UserName}')
        if 'i' in ask_time:
            i_time = strftime("%Y , %m , %d", localtime())
            print('Now is : (', i_time, f') {UserName}')


class start:
    """
        Star class
        In this class there are start methods
    """

    @staticmethod
    def start():
        start_list = [
            f'Welcome back {UserName} !',
            f'Hi {UserName} !',
            f'Hello {UserName} ! I missed U :)'
            f'Hi Honey !'
        ]
        print(random.choice(start_list))
        print(f'Today is : (', strftime("%Y , %m , %d", localtime()), f') {UserName}')

    @staticmethod
    def hello():
        hello_list = [
            f'Hello {UserName} !',
            'Hi Darline !',
            'Hello my love !',
            f'Welcome Back {UserName} .'
        ]
        print(random.choice(hello_list))


class close:
    """
        Close class
        Here are methods for ending app
    """

    @staticmethod
    def bye():
        bye_list = [
            'bye sweetie .',
            f'Bye {UserName}'
        ]
        print(random.choice(bye_list))

    @staticmethod
    def Goodnight():
        print(f'Have a Good night {UserName}.')
        print('I hope you sleep well!')

    @staticmethod
    def Sleep():
        print('Oh , OK !')
        print('Goodbye Pal !')


class cli:
    """
        CLI class
        We have cli stuff here. Like clear or change bg color
    """

    @staticmethod
    def clear():
        os.system("clear")


class software:
    """
        Software class
        Uninstall, Update and other software methods are here
    """

    version = 'Rachel is V 0.1.0 !'

    @staticmethod
    def uninstall():
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
