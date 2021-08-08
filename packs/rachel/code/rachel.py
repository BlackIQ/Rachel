"""
    Rachel

    Written by -> Amirhossein Mohammadi & Erfan Saberi
    github.com/BlackIQ
    github.com/erfansaberi

    Rachel's Version -> 0.0.1
"""

import sys

sys.path.append('usr/app')

# Import Brain
from libra.core import *
from libra.data import *

while True:

    q = input(f'What can I do for you {firstname} ? ')
    if not q:
        pass
    # { ----- Start ----- } Commands
    elif 'uninstall' in q:
        software.uninstall()
    elif 'version' in q:
        print(software.version)
    elif 'hello' in q:
        start.hello()
    elif 'hi' in q:
        start.hello()
    elif 'clear' in q:
        cli.clear()

    # { StarDate } Command
    elif 'stardate' in q:
        StarDate()
    # { Date } Command
    elif 'date' in q:
        dt.Date()
    elif 'what date is today' in q:
        dt.Date()
    elif 'today' in q:
        dt.Date()
    # { Time } Command
    elif 'time' in q:
        dt.Time()
    elif 'what time is it' in q:
        dt.Time()
    elif 'now' in q:
        dt.Time()
    # { ----- End  ----- } Commands
    # { Close } Command
    elif 'close' in q:
        close.bye()
        break
    elif 'exit' in q:
        close.bye()
        break
    # { Sleep ) Command
    elif 'sleep' in q:
        close.Sleep()
        break
    # { Good night } Command
    elif 'good night' in q:
        close.Goodnight()
        break
    # { Bye } Command
    elif 'bye' in q:
        close.bye()
        break

    # { ----- Chat ----- } Command
    else:
        print('Sorry, i didnt understand . do you want me to search it in the internet ?')
        p = input('[Y]es , [N]o : ')
        if p == 'y':
            print(search_in_net(q))
        else:
            pass

input()
