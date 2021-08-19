"""
    Rachel

    Written by -> Amirhossein Mohammadi & Erfan Saberi
    github.com/BlackIQ
    github.com/erfansaberi

    Powered by PyAbr
    PyAbr by Mani Jamali

"""

import RachelCore

while True:
    # Get input
    user_command = str(input("What can I do?"))
    # Move it to Core
    RachelCore.command.get(user_command)
