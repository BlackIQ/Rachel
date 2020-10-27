"""
    Rachel's Data reader from database

    Written by -> Mani Jamali
    github.com/manijamali2003

    Rachel's Version -> 0.0.1
    Data's  Version -> 0.0.1
"""

# Use PyAbr Database Extensions
from libabr.control import read_record

# Read From database
UserName = read_record('username' , 'database')
firstname = read_record('firstname' , 'database')
lastname = read_record('lastname' , 'database')
email = read_record('email' , 'database')
phone = read_record('phone' , 'database')