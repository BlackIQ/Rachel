"""
    Rachel

    Written by -> Amirhossein Mohammadi & Erfan Saberi
    github.com/BlackIQ
    github.com/erfansaberi

    Powered by PyAbr
    PyAbr by Mani Jamali

"""

import RachelCore
import sys

try:
    if sys.argv[1] == "--update":
        RachelCore.software.update()
    if sys.argv[1] == "--uninstall":
        RachelCore.software.uninstall()
    if sys.argv[1] == "version":
        print(RachelCore.software.version)
except:
    pass

while True:
    # Get input
    RachelCore.command.get()
