# Import Brain
from Core import *

# Start
start()

while True:

    q = input(f'What can I do for you {username} ? ')
    if not q:
        pass
    # { ----- Start ----- } Commands
    elif 'hello' in q:
        hello()
    elif 'hi' in q:
        hello()
    elif 'clear' in q:
        clear()
    # { StarDate } Command
    elif 'stardate' in q:
        StarDate()
    # { Date } Command
    elif 'date' in q :
        Date()
    elif 'what date is today' in q :
        Date()
    elif 'today' in q :
        Date()
    # { Time } Command
    elif 'time' in q :
        Time()
    elif 'what time is it' in q :
        Time()
    elif 'now' in q :
        Time()
    # { ----- End  ----- } Commands
    # { Close } Command
    elif 'close' in q:
        bye()
        break
    elif 'exit' in q :
        bye()
        break
    # { Sleep ) Command
    elif 'sleep' in q:
        Sleep()
        break
    # { Good night } Command
    elif 'good night' in q:
        Goodnight()
        break
    # { Bye } Command
    elif 'bye' in q:
        bye()
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