"""
    Rachel's Setup written by Amirhossein Mohammadi
    github.com/BlackIQ/Rachel
    
    Version -> not available
"""

# MySQL.connector -> Make connection between Python & MySQL
import mysql.connector

# getpass -> get password hidden
from getpass import getpass

# Termcolor -> Make output colored
from termcolor import colored

# Write Data into File
def w(Firstname , Lastname , Age , Username , Password) :
    # Open File
    print("Openning File . . .")
    write = open("Data.py", "w")

    # Write
    print("Saving at Data.py . . .")
    write.write(f"FirstName = '{Firstname}'")
    write.write("\n")
    write.write(f"LastName = '{Lastname}'")
    write.write("\n")
    write.write(f"Age = '{Age}'")
    write.write("\n")
    write.write(f"UserName = '{Username}'")
    write.write("\n")
    write.write(f"Password = '{Password}'")

    # Close File
    write.close()

# Start The Config
print("Welcome To Rachel User Config !")
print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

# Get MySQL Data
print("Right now , Enter MySQL Data\n")
mysqlhost = str(input("What is your Host ? [127.0.0.1] : "))
mysqluser = str(input("What is MySQL User ? [Rachel] : "))
mysqlpassword = getpass("What is MySQL Password ? [Rachel] : ")

# Start User Data
print("- - - - - - - - - - - - - - - - - - - -")
print("Right now , Enter You personal Data\n")
Firstname = str(input("What is your First Name ? "))
Lastname = str(input("What is your Last Name ? "))
Age = str(input("How old are you ? "))
Username = str(input("What you wana choose as your Username ? "))
Password = getpass("What you wana choose as your Password ? ")

print("- - - - - - - - - - - - - - - - - - - -")
print("Connecting to MySQL . . .\n")

# Connect to MySQL
cnx = mysql.connector.connect(
    user = mysqluser ,
    password = mysqlpassword ,
    host = mysqlhost
)

# Set a cursor
cursor = cnx.cursor()

print("Creating and Inserting to Database . . .")

# MySQL Stuff
cursor.execute('DROP DATABASE Amir')
cursor.execute('CREATE DATABASE Amir')
cursor.execute('USE Amir')
cursor.execute('CREATE TABLE Data (Firstname TEXT , Lastname TEXT , Age TEXT , Username TEXT , Password TEXT)')
cursor.execute(f"INSERT INTO Data VALUES ('{Firstname}' , '{Lastname}' , '{Age}' , '{Username}' , '{Password}')")

# Commit CNX
cnx.commit()

print("Everything Inserted")

# Read from Database ( Executing )
cursor.execute("SELECT * FROM Data")

# Reading Loop
print("- - - - - - - - - - - - - - - - - - - -")
for (fname , lname , age , username , password) in cursor :
    # Write at Data.py
    w(fname , lname , age , username , password)

# Close CNX
print("All Done !")
cnx.close()