"""
    Rachel's Data reader from database

    Written by -> Mani Jamali
    github.com/manijamali2003

    Rachel's Version -> 0.0.1
    Data's  Version -> 0.0.1
"""

# Use PyAbr Database Extensions

from libabr import Files, Control
# Read From database
files = Files()
control = Control()

UserName = ''
firstname = ''
lastname = ''
email = ''
phone = ''

## Use default Pyabr database ##
if files.isfile ('/proc/info/su'):
    UserName = files.readall('/proc/info/su')
    firstname = control.read_record('first_name','/etc/users/'+UserName)
    lastname = control.read_record('last_name', '/etc/users/' + UserName)
    email = control.read_record('email', '/etc/users/' + UserName)
    phone = control.read_record('phone', '/etc/users/' + UserName)
else:
## Use internal Rachel database ##
    UserName = control.read_record('username' , '/etc/rachel')
    firstname = control.read_record('firstname' , '/etc/rachel')
    lastname = control.read_record('lastname' , '/etc/rachel')
    email = control.read_record('email' , '/etc/rachel')
    phone = control.read_record('phone' , '/etc/rachel')