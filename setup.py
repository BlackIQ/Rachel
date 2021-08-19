import os

os.system("gcc Rachel/execute.c")
os.system("mkdir exe")
os.system("cp -r a.out exe")
os.system("mv exe/a.out exe/Rachel")
os.system("cp -r exe/Rachel /bin")
os.system("mkdir ~/Rachel")
os.system("cp -r Rachel/rachel.py ~/Rachel")

print("done.")