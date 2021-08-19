import os

print("Begin installation.")

os.system("gcc Rachel/execute.c")
os.system("mkdir exe")
os.system("cp -r a.out exe")
os.system("mv exe/a.out exe/Rachel")
os.system("sudo cp -r exe/Rachel /bin")
os.system("mkdir ~/.Rachel")
os.system("cp -r Rachel/rachel.py ~/.Rachel")
os.system("rm -rf exe a.out")
os.system("pip3 install RachelCore")

print("Installation done.")
