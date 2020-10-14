# Import Brain
from Brain import *

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
    elif 'date' or 'what date is today' or 'today' in q:
        Date()
    # { Time } Command
    elif 'time' or 'what time is it' or 'now' in q:
        Time()

    # { ----- End  ----- } Commands
    # { Close } Command
    elif 'close' or 'exit' in q:
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
        answer = chat(q)
        if answer:
            print(answer)
        else:
            print('Sorry, i didn\'t understand what you want from me, do you want me to search it in the internet?')
            p = input('y/n: ')
            if p == 'y':
                print(search_in_net(q))
            else:
                pass
input()