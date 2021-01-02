#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

import importlib, shutil, os, sys, hashlib, subprocess,time,datetime,getpass,py_compile, site

# script #
class Script:
    def __init__(self,filename):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        # check perms #
        if not permissions.check(files.output(filename) + '.sa', "x", files.readall("/proc/info/su")):
            colors.show(filename, "perm", "")
            sys.exit(0)

        cmdall = control.read_list(filename + '.sa') # read all lines from script

        k = 0

        for cmd in cmdall:
            k = k + 1
            ## Create cmdln with variables ##
            cmdln = cmd.split(" ")

            strcmdln = ""

            for i in cmdln:
                if str(i).startswith("$"):
                    select = files.readall("/proc/info/sel")
                    var = control.read_record(str(i).replace("$", ""), select)
                    if var == None:
                        strcmdln = strcmdln + " " + i
                    else:
                        strcmdln = strcmdln + " " + var
                else:
                    strcmdln = strcmdln + " " + i

            cmdln = strcmdln.split(" ")
            cmdln.remove('')

            cmd = ""
            for j in cmdln:
                cmd = cmd + " " + j

            if (cmdln == [] or
                    cmdln[0] == "" or
                    cmdln[0] == " " or
                    cmd.startswith("#") or
                    cmd.startswith("//") or
                    (cmd.startswith("/*") and cmd.endswith("*/")) or
                    (cmd.startswith("\'\'\'") and cmd.endswith("\'\'\'")) or
                    cmd.startswith(";")
            ):
                continue
            else:
                System(cmd)

# commands #
class Commands:
    def __init__(self):
        pass

    def unset(self,args):
        files = Files()
        control = Control()
        permissions = Permissions()
        colors = Colors()
        for name in args:
            select = files.readall("/proc/info/sel")
            if not select.startswith("/proc/"):
                if permissions.check(files.output(select), "w", files.readall("/proc/info/su")):
                    control.remove_record(name, select)
                else:
                    colors.show("unset", "perm", "")
            else:
                control.remove_record(name, select)
    # cc command #
    def cc (self,args):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control()
        # args #

        if args==[]:
            colors.show('cc','fail','no inputs.')
            sys.exit(0)

        # args after checking #
        filename = args[0]
        # check file #
        type = None

        # check file #
        if not files.isfile (filename):
            colors.show ('cc','fail',filename+": file not found.")
            sys.exit(0)

        if files.isdir (filename):
            colors.show('cc','fail',filename+": is a directory.")
            sys.exit(0)

        # check permission of filename to read #
        if not permissions.check(files.output(filename), "r", files.readall("/proc/info/su")):
            colors.show('cc','perm','')
            sys.exit(0)

        if filename.endswith ('.c'):
            type = 'c'
        elif filename.endswith ('.cpp') or filename.endswith('.c++') or filename.endswith('.cxx'):
            type = 'c++'
        elif filename.endswith ('.py'):
            type = 'python'
        elif filename.endswith ('.java'):
            type = 'java'

        # compile types #
        if type=='python':
            if args[1:]==[]:
                py_compile.compile(files.input(filename),files.input(filename.replace('.py','.pyc')))
                if not permissions.check(files.output(filename.replace('.py','.pyc')), "w", files.readall("/proc/info/su")):
                    colors.show('cc', 'perm', '')
                    sys.exit(0)
            else:
                output = args[1]
                if not permissions.check(files.output(output), "w", files.readall("/proc/info/su")):
                    colors.show('cc', 'perm', '')
                    sys.exit(0)
                py_compile.compile(files.input(filename), files.input(output))


        elif type=='c':
            if args[1:] == []:
                output = filename.replace('.c','')
            else:
                output = args[1]

            if not permissions.check(files.output(output), "w", files.readall("/proc/info/su")):
                colors.show('cc', 'perm', '')
                sys.exit(0)

            strv = control.read_record('exec.c','/etc/compiler').replace ("{src}",files.input(filename)).replace ("{dest}",files.input(output))

            strv = strv.split(" ")

            subprocess.call(strv)


        elif type=='c++':
            if args[1:] == []:
                output = filename.replace('.c','').replace('.cpp','').replace('.cxx','')
            else:
                output = args[1]

            if not permissions.check(files.output(output), "w", files.readall("/proc/info/su")):
                colors.show('cc', 'perm', '')
                sys.exit(0)

            strv = control.read_record('exec.c++', '/etc/compiler').replace("{src}", files.input(filename)).replace(
                "{dest}", files.input(output)).split (" ")

            subprocess.call(strv)


        elif type=='java':
            if not permissions.check(files.output(filename.replace('.java','.class')), "w", files.readall("/proc/info/su")):
                colors.show('cc', 'perm', '')
                sys.exit(0)


            strv = (control.read_record('class.java', '/etc/compiler').replace("{src}", files.input(filename).replace('.//',''))).split (' ')
            subprocess.call(strv)
        else:
            colors.show('cc','fail','not supported programing language.')

    # check command #
    def check (self,args):
        filename = args[0]
        permissions = Permissions()
        files = Files()
        colors = Colors()

        perm = permissions.get_permissions(files.output(filename))
        numperm = permissions.show_number(perm)
        r = permissions.check(files.output(filename), "r", files.readall("/proc/info/su"))
        w = permissions.check(files.output(filename), "w", files.readall("/proc/info/su"))
        x = permissions.check(files.output(filename), "x", files.readall("/proc/info/su"))

        bold = colors.color(1, colors.get_bgcolor(), colors.get_fgcolor())

        print("   Seleted path: " + bold + files.output(filename) + colors.get_colors())
        print("     Permission: " + bold + perm + colors.get_colors())
        print(" Permission Num: " + bold + str(numperm) + colors.get_colors())
        if r == True:
            print("           Read: " + bold + colors.get_ok() + "Yes" + colors.get_colors())
        else:
            print("           Read: " + bold + colors.get_fail() + "No" + colors.get_colors())

        if w == True:
            print("          Write: " + bold + colors.get_ok() + "Yes" + colors.get_colors())
        else:
            print("          Write: " + bold + colors.get_fail() + "No" + colors.get_colors())

        if x == True:
            print("        Execute: " + bold + colors.get_ok() + "Yes" + colors.get_colors())
        else:
            print("        Execute: " + bold + colors.get_fail() + "No" + colors.get_colors())

    # chmod command #
    def chmod (self,args):

        mod = args[0]
        filename = args[1]
        permissions = Permissions()
        files = Files()
        colors = Colors()

        if args==[] or args[1:]==[]:
            colors.show("chmod", "fail", "no inputs.")
            sys.exit(0)

        perm_user = int(mod[0])
        perm_others = int(mod[1])
        perm_guest = int(mod[2])
        if permissions.check_owner(files.output(filename), files.readall("/proc/info/su")):
            owner = permissions.get_owner(files.output(filename))
            permissions.create(files.output(filename), perm_user, perm_others, perm_guest, owner)
        else:
            colors.show("chmod", "perm", "")

    # chown #
    def chown (self,args):
        new_owner = args[0]
        name = args[1]
        permissions = Permissions()
        files = Files()
        colors = Colors()

        if args==[]:
            colors.show("chown", "fail", "no inputs.")
            sys.exit(0)

        if args[1:]==[]:
            new_owner = ''

        permowner = permissions.check_owner(files.output(name), files.readall("/proc/info/su"))
        perm = permissions.get_permissions(files.output(name))

        num = permissions.show_number(perm)
        num = str(num)
        user_p = int(num[0])
        others_p = int(num[1])
        guest_p = int(num[2])

        if permowner == True:
            if new_owner == "":
                permissions.create(files.output(name), user_p, others_p, guest_p, files.readall("/proc/info/su"))
            else:
                permissions.create(files.output(name), user_p, others_p, guest_p, new_owner)
        else:
            colors.show("chown", "perm", "")

    # logout #
    def logout (self,args):
        files = Files()
        colors = Colors()
        process = Process()

        if files.isfile("/proc/selected"): files.remove("/proc/selected")
        process.endall()
        subprocess.call([sys.executable,files.readall("/proc/info/boot"), 'login'])

    # new #
    def new (self,args):
        colors = Colors()
        files = Files()
        control = Control()

        boot = files.readall("/proc/info/boot")

        user = control.read_record("username", "/tmp/su.tmp")
        code = control.read_record ("code","/tmp/su.tmp")

        if files.isfile("/proc/selected"): files.remove("/proc/selected")
        if user == "guest":
            subprocess.call([sys.executable,boot, 'user', 'guest'])
        else:
            subprocess.call([sys.executable,boot, 'user', user, code])

    # reboot #
    def reboot (self,args):
        colors = Colors()
        files = Files()
        process = Process()

        if files.isfile("/proc/selected"): files.remove("/proc/selected")
        colors.show("kernel", "reboot", "")
        if files.isdir("/desk/guest"):
            files.removedirs("/desk/guest")
        if files.isdir("/tmp"):
            files.removedirs("/tmp")
            files.mkdir("/tmp")
        process.endall()
        subprocess.call([sys.executable,files.readall("/proc/info/boot")])

    # shut command #
    def shut (self,args):
        colors = Colors()
        control = Control()
        files = Files()
        process = Process()

        if files.isfile("/proc/selected"): files.remove("/proc/selected")
        process.end(int(files.readall("/proc/info/sp")))

        if files.readall("/proc/info/su") == "0":
            if files.isdir("/desk/guest"):
                files.removedirs("/desk/guest")
            if files.isdir("/tmp"):
                files.removedirs("/tmp")
                files.mkdir("/tmp")
            if files.isfile("/proc/selected"): files.remove("/proc/selected")
            process.endall()

    # shutdown command #
    def shutdown (self,args):
        colors = Colors()
        control = Control()
        files = Files()
        process = Process()

        if files.isdir("/desk/guest"):
            files.removedirs("/desk/guest")
        if files.isdir("/tmp"):
            files.removedirs("/tmp")
            files.mkdir("/tmp")
        if files.isfile("/proc/selected"): files.remove("/proc/selected")
        process.endall()

    # ver command #
    def ver (self,args):
        colors = Colors()
        control = Control()
        files = Files()
        process = Process()

        bold = colors.color(1, colors.get_bgcolor(), colors.get_fgcolor())

        print("        Static hostname: " + bold + files.readall("/proc/info/host") + colors.get_colors())
        print("         cloud Software: " + bold + files.readall("/proc/info/cs") + " " + files.readall(
            "/proc/info/ver") + " (" + files.readall("/proc/info/cd") + ")" + colors.get_colors())
        print("             Build date: " + bold + files.readall("/proc/info/bl") + colors.get_colors())
        print("       Operating System: " + bold + files.readall("/proc/info/os") + colors.get_colors())
        print("                 Kernel: " + bold + files.readall("/proc/info/kname") + " " + files.readall(
            "/proc/info/kver") + colors.get_colors())
        print("          Switched User: " + bold + files.readall("/proc/info/su") + colors.get_colors())
        print("       Switched Process: " + bold + files.readall("/proc/info/sp") + colors.get_colors())

        print("           Architecture: " + bold + files.readall('/proc/info/arch') + colors.get_colors())

    # cat command #
    def cat (self,args):
        colors = Colors()
        control = Control()
        files = Files()
        process = Process()
        permissions = Permissions()

        ## args ##

        name = None
        option = None

        cmdln = ['']
        cmdln[1:] = args

        if not cmdln[1:] == []:
            if cmdln[1] == '-r' or cmdln[1] == '-c' or cmdln[1] == '-w' or cmdln[1] == '-a' or cmdln[1]=='-l':
                option = cmdln[1]
                name = cmdln[2]
            else:
                name = cmdln[1]
                option = ''
        else:
            colors.show("cat", "fail", "no inputs.")
            sys.exit(0)

        ## Read files ##
        if option == '' or option == '-r':
            if files.isfile(name):
                if permissions.check(files.output(name), "r", files.readall("/proc/info/su")):
                    file = open(files.input(name), "rb")
                    check_bin = str(file.read())
                    file.close()
                    if check_bin.__contains__("\\x00"):
                        print(check_bin)
                    else:
                        print(files.readall(name))
                else:
                    colors.show("cat", "perm", "")
            elif files.isdir(name):
                colors.show("cat", "fail", name + ": is a directory.")
            else:
                colors.show("cat", "fail", name + ": file not found.")

        ## Create files ##
        elif option == '-c':
            if files.isdir(name):
                colors.show("cat", "fail", name + ": is a directory.")
            else:
                if permissions.check(files.output(name), "w", files.readall("/proc/info/su")):
                    files.create(name)
                else:
                    colors.show("cat", "perm", "")

        ## Write in lines
        elif option == '-l':
            if files.isdir(name):
                colors.show("cat", "fail", name + ": is a directory.")
            else:
                if permissions.check(files.output(name), "w", files.readall("/proc/info/su")):
                    strv = ''
                    for i in cmdln[3:]:
                        strv+=' '+i
                    files.write(name,strv[1:])
                else:
                    colors.show("cat", "perm", "")

        ## Write into files ##
        elif option == '-w':
            if files.isdir(name):
                colors.show("cat", "fail", name + ": is a directory.")
            else:
                if permissions.check(files.output(name), "w", files.readall("/proc/info/su")):

                    ## Set EOF
                    if cmdln[3:] == []:
                        EOF = 'EOF'
                    else:
                        EOF = cmdln[3]

                    # WRITE COMMAND LINE

                    texts = ''

                    while True:
                        cmd = input('> ')
                        if cmd == EOF:
                            break
                        else:
                            if texts == '':
                                texts = cmd
                            else:
                                texts = texts + '\n' + cmd

                    ## WRITE INTO FILE
                    files.write(cmdln[2], texts)
                else:
                    colors.show("cat", "perm", "")

        ## Write into files ##
        elif option == '-a':
            if files.isdir(name):
                colors.show("cat", "fail", name + ": is a directory.")
            else:
                if permissions.check(files.output(name), "w", files.readall("/proc/info/su")):

                    ## Set EOF
                    if cmdln[3] == []:
                        EOF = 'EOF'
                    else:
                        EOF = cmdln[3]

                    # WRITE COMMAND LINE

                    texts = ''

                    while True:
                        cmd = input('> ')
                        if cmd == EOF:
                            break
                        else:
                            if texts == '':
                                texts = cmd
                            else:
                                texts = texts + '\n' + cmd

                    ## WRITE INTO FILE
                    files.append(cmdln[2], texts)
                else:
                    colors.show("cat", "perm", "")

    # cd command #
    def cd (self,args):
        permissions = Permissions()
        files = Files()
        colors = Colors()

        if args==[]:
            colors.show("cd", "fail", "no inputs.")
            sys.exit (0)

        path = args[0]

        if permissions.check(files.output(path), "r", files.readall("/proc/info/su")):
            if path == '..':
                pwd = files.readall('/proc/info/pwd')
                pwd = pwd.split('/')
                lens = len(pwd) - 1
                pwd.pop(lens)

                strv = ''

                for i in pwd:
                    strv += "/" + i

                pwd = files.output_shell(strv)
                files.write("/proc/info/pwd", pwd)
            elif files.isdir(path):
                files.write("/proc/info/pwd", files.output_shell(path))
            else:
                colors.show("cd", "fail", path + ": directory not found.")
        else:
            colors.show("cd", "perm", "")

    # clean command #
    def clean (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        user = files.readall("/proc/info/su")
        select = files.readall("/proc/info/sel")

        if not select.startswith("/proc/"):
            if permissions.check(files.output(select), "w", user):
                files.create(select)
            else:
                colors.show("clean", "perm", "")
        else:
            files.create(select)

    # clear command #
    def clear (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        osname = files.readall("/proc/info/os")
        if osname == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    # cp command #
    def cp (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        # args #
        cmdln = ['']
        cmdln[1:] = args

        if cmdln[1:] == []:
            colors.show("cp", "fail", "no inputs.")
        if cmdln[2:] == []:
            colors.show("cp", "fail", "no inputs.")

        src = cmdln[1]
        dest = cmdln[2]



        if files.isdir(src):
            if files.isfile(dest):
                colors.show("cp", "fail", dest + ": dest is a file.")
            else:
                if permissions.check(files.output(src), "r", files.readall("/proc/info/su")):
                    if permissions.check(files.output(dest), "w", files.readall("/proc/info/su")):
                        perm = permissions.get_permissions(files.output(src))
                        control.write_record(files.output(dest), perm, "/etc/permtab")
                        files.copydir(src, dest)

                    else:
                        colors.show("cp", "perm", "")
                else:
                    colors.show("cp", "perm", "")
        elif files.isfile(src):
            if files.isdir(dest):
                colors.show("cp", "fail", dest + ": dest is a directory.")
            else:
                if permissions.check(files.output(src), "r", files.readall("/proc/info/su")):
                    if permissions.check(files.output(dest), "w", files.readall("/proc/info/su")):
                        perm = permissions.get_permissions(files.output(src))
                        control.write_record(files.output(dest), perm, "/etc/permtab")
                        files.copy(src, dest)
                    else:
                        colors.show("cp", "perm", "")
                else:
                    colors.show("cp", "perm", "")
        else:
            colors.show("cp", "fail", src + ": source not found.")

    # date command #
    def date (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        ## Show all time and date ##
        if args == []:
            os.environ['TZ'] = files.readall("/proc/info/tz")  # https://stackoverflow.com/questions/1301493/setting-timezone-in-python
            time.tzset()
            print(datetime.datetime.now().ctime())

        ## Show utc now ##
        if args == ['utc']:
            print(datetime.datetime.utcnow().ctime())

    # getv command #
    def getv (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        select = files.readall("/proc/info/sel")
        if not select.startswith("/proc/"):
            if permissions.check(files.output(select), "w", files.readall("/proc/info/su")):
                listinfo = files.list("/proc/info")
                for i in listinfo:
                    control.write_record(i, files.readall("/proc/info/" + i), select)
            else:
                colors.show("getv", "perm", "")
        else:
            listinfo = files.list("/proc/info")
            for i in listinfo:
                control.write_record(i, files.readall("/proc/info/" + i), select)

    # help command #
    def help (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args==[]:
            print(files.readall("/usr/share/helps/cmdall.txt"))
        else:
            if files.isfile("/usr/share/helps/" + args[0] + ".txt"):
                print(files.readall("/usr/share/helps/" + args[0] + ".txt"))
            else:
                print(files.readall("/usr/share/helps/cmdall.txt"))

    # read command #
    def read (self,args):
        for i in args:
            self.set([i+":",input()])

    # ls command #
    def ls (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        path = None
        options = None

        # check args #

        if not args == [] and args[1:] == []:
            path = files.output(args[0])
            options = ''
        elif not args == [] and not args[1:] == []:
            path = files.output(args[0])
            options = args[1]
        elif args == []:
            path = files.readall("/proc/info/pwd")
            options = ''

        if options == "":
            if files.isdir(path):
                if permissions.check(files.output(path), "r", files.readall("/proc/info/su")):
                    list = files.list(path)
                    list.sort()
                    for i in list:
                        if files.isdir(path + "/" + i):
                            print(colors.get_path() + i + "/" + colors.get_colors())
                        else:
                            print(i)
                else:
                    colors.show("ls", "perm", "")
            else:
                colors.show("ls", "fail", path + ": directory not found.")
        elif options == "-p":
            if files.isdir(path):
                if permissions.check(files.output(path), "r", files.readall("/proc/info/su")):
                    list = files.list(path)
                    list.sort()
                    for i in list:
                        if files.isdir(path + "/" + i):
                            perm = permissions.get_permissions(path + "/" + i)
                            print(perm + "\t" + colors.get_path() + i + "/" + colors.get_colors())
                        else:
                            perm = permissions.get_permissions(path + "/" + i)
                            print(perm + "\t" + i)
                else:
                    colors.show("ls", "perm", "")
            else:
                colors.show("ls", "fail", path + ": directory not found.")
        elif options == "-n":
            if files.isdir(path):
                if permissions.check(files.output(path), "r", files.readall("/proc/info/su")):
                    list = files.list(path)
                    list.sort()
                    for i in list:
                        if files.isdir(path + "/" + i):
                            perm = permissions.get_permissions(path + "/" + i)
                            perm = str(permissions.show_number(perm))
                            print(perm + "\t" + colors.get_path() + i + "/" + colors.get_colors())
                        else:
                            perm = permissions.get_permissions(path + "/" + i)
                            perm = str(permissions.show_number(perm))
                            print(perm + "\t" + i)
                else:
                    colors.show("ls", "perm", "")
            else:
                colors.show("ls", "fail", path + ": directory not found.")

    # mkdir command #
    def mkdir (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        for i in args:
            if files.isfile(i):
                colors.show("mkdir", "fail", i + ": is a file.")
            elif files.isdir(i):
                colors.show("mkdir", "warning", i + ": directory exists.")
            else:
                if permissions.check(files.output(i), "w", files.readall("/proc/info/su")):
                    files.makedirs(i)
                else:
                    colors.show("mkdir", "perm", "")

    # mv command #
    def mv (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        # args #
        cmdln = ['']
        cmdln[1:] = args

        if cmdln[1:] == []:
            colors.show("mv", "fail", "no inputs.")
        if cmdln[2:] == []:
            colors.show("mv", "fail", "no inputs.")

        src = cmdln[1]
        dest = cmdln[2]

        if files.isdir(src):
            if files.isfile(dest):
                colors.show("mv", "fail", dest + ": dest is a file.")
            else:
                if permissions.check(files.output(src), "r", files.readall("/proc/info/su")) and permissions.check(
                        files.output(src), "w", files.readall("/proc/info/su")):
                    if permissions.check(files.output(dest), "w", files.readall("/proc/info/su")):
                        perm = permissions.get_permissions(files.output(src))
                        control.write_record(files.output(dest), perm, "/etc/permtab")
                        files.copydir(src, dest)
                        files.removedirs(src)
                    else:
                        colors.show("mv", "perm", "")
                else:
                    colors.show("mv", "perm", "")
        elif files.isfile(src):
            if files.isdir(dest):
                colors.show("mv", "fail", dest + ": dest is a directory.")
            else:
                if permissions.check(files.output(src), "r", files.readall("/proc/info/su")) and permissions.check(
                        files.output(src), "w", files.readall("/proc/info/su")):
                    if permissions.check(files.output(dest), "w", files.readall("/proc/info/su")):
                        perm = permissions.get_permissions(files.output(src))
                        control.write_record(files.output(dest), perm, "/etc/permtab")
                        files.copy(src, dest)
                        files.remove(src)
                    else:
                        colors.show("mv", "perm", "")
                else:
                    colors.show("mv", "perm", "")
        else:
            colors.show("mv", "fail", src + ": source not found.")

    # echo command #
    def echo (self,args):
        for i in args:
            print(
                i
                    .replace("-a", "\a")
                    .replace("-b", "\b")
                    .replace("-f", "\f")
                    .replace("-n", "\n")
                    .replace("-r", "\r")
                    .replace("-t", "\t")
                    .replace("-v", "\v"), end=' ')
        print()

    # rm command #
    def rm (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        for i in args:
            if files.isdir(i):
                if permissions.check(files.output(i), "w", files.readall("/proc/info/su")):
                    files.removedirs(i)
                    control.remove_record(i,'/etc/permtab')
                else:
                    colors.show("rm", "perm", "")
                    sys.exit(0)
            elif files.isfile(i):
                if permissions.check(files.output(i), "w", files.readall("/proc/info/su")):
                    files.remove(i)
                    control.remove_record(i, '/etc/permtab')
                else:
                    colors.show("rm", "perm", "")
                    sys.exit(0)
            else:
                colors.show("rm", "fail", i + ": file or directory not found.")
                sys.exit(0)

    ## mount ##

    def mount (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        ## Check root ##
        if not permissions.check_root(files.readall("/proc/info/su")):
            colors.show("mount", "perm", "")
            sys.exit(0)

        ## Check inputs ##
        if args==[] or args[1:]==[]:
            colors.show("mount", "fail", "no inputs.")
            sys.exit(0)

        src = args[0]
        dest = args[1]

        ## already mounted ##
        if files.readall('/etc/fstab') == src:
            colors.show('mount','warning',src+": was already mounted.")
            sys.exit(0)

        ## Check block ##
        if not files.isfile (src):
            colors.show("mount", "fail", "unknown device block.")
            sys.exit(0)

        # check dest #
        if files.isfile (dest):
            colors.show("mount", "fail", dest+": dest is a file.")
            sys.exit(0)

        if not files.isdir(dest): files.mkdir(dest)

        # get raw #

        control.write_record(dest,src,'/etc/fstab')

    def umount (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        ## Check root ##
        if not permissions.check_root(files.readall("/proc/info/su")):
            colors.show("umount", "perm", "")
            sys.exit(0)

        ## Check inputs ##
        if args == []:
            colors.show("umount", "fail", "no inputs.")
            sys.exit(0)

        ## check mount point ##
        if not files.readall('/etc/fstab')==args[0]:
           colors.show('umount','fail',args[0]+': mount point not found.')
           sys.exit(0)

        ## not done ##

    ## passwd ##
    def passwd (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args==[]:
            colors.show('passwd','fail','no inputs.')
            sys.exit(0)

        user = args[0]

        # check user exists
        if not files.isfile('/etc/users/'+user):
            colors.show('passwd', 'fail', user+": user not found.")
            sys.exit(0)

        # check user exists with hashname

        username = control.read_record('username','/etc/users/'+user)
        hashname = hashlib.sha3_256(user.encode()).hexdigest()

        if not username==hashname:
            colors.show('passwd', 'fail', user + ": user not found.")
            sys.exit(0)

        # old password

        code = control.read_record('code','/etc/users/'+user)

        oldcode = hashlib.sha3_512(getpass.getpass('Enter '+user+"'s old password: ").encode()).hexdigest()

        if not code==oldcode:
            colors.show('passwd', 'fail', user + ": wrong password.")
            sys.exit(0)

        newcode = getpass.getpass('Enter a new password: ')

        while True:
            confirm = getpass.getpass('Confirm the new password: ')
            if confirm==newcode: break
            else:
                print('Try agian!')

        control.write_record('code',hashlib.sha3_512(newcode.encode()).hexdigest(),'/etc/users/'+user)

    # say command #
    def say (self,args):
        for i in args:
            print(
                i
                    .replace("-a", "\a")
                    .replace("-b", "\b")
                    .replace("-f", "\f")
                    .replace("-n", "\n")
                    .replace("-r", "\r")
                    .replace("-t", "\t")
                    .replace("-v", "\v"), end=' ')

    # sel command #
    def sel (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == []:
            colors.show("sel", "fail", "no inputs.")
            sys.exit(0)

        database_name = args[0]

        if files.isfile(database_name):
            if permissions.check(files.output(database_name), "r", files.readall("/proc/info/su")):
                files.write("/proc/info/sel", database_name)
                files.create("/proc/selected")
            else:
                colors.show("sel", "perm", "")
        else:
            colors.show("sel", "fail", database_name + ": controller not found.")

    # set command #
    def set (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == [] or args[1:] == []:
            colors.show("set", "fail", "no inputs.")
            sys.exit(0)

        if not args[0].endswith(":"):
            colors.show("set", "fail", "wrong syntax.")
            sys.exit(0)

        name = args[0].replace(":", "")
        value = args[1]

        select = files.readall("/proc/info/sel")
        if not select.startswith("/proc/"):
            if permissions.check(files.output(select), "w", files.readall("/proc/info/su")):
                control.write_record(name, value, select)
            else:
                colors.show("set", "perm", "")
        else:
            control.write_record(name, value, select)

    # sleep command #
    def sleep (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == []:
            time.sleep(3)
        else:
            timeout = float(args[0])
            time.sleep(int(timeout))

    # su command #
    def su (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == []:
            colors.show("su", "fail", "no inputs.")
            sys.exit(0)

        input_username = args[0]
        user = files.readall("/proc/info/su")

        if files.isfile("/proc/selected"): files.remove("/proc/selected")
        if user == input_username:
            colors.show("su", "warning", user + " has already switched.")
        elif input_username == "guest":
            enable_cli = control.read_record("enable_cli", "/etc/guest")
            if enable_cli == "Yes":
                subprocess.call ([sys.executable,files.readall("/proc/info/boot"),'user','guest'])
            else:
                colors.show(input_username, "fail", "user not found.")

        elif files.isfile("/etc/users/" + input_username):
            hashname = hashlib.sha3_256(str(input_username).encode()).hexdigest()
            username = control.read_record("username", "/etc/users/" + input_username)
            if hashname == username:
                input_password = getpass.getpass('Enter ' + input_username + '\'s password: ')
                hashcode = hashlib.sha3_512(str(input_password).encode()).hexdigest()
                password = control.read_record("code", "/etc/users/" + input_username)
                if hashcode == password:
                    subprocess.call ([sys.executable,files.readall("/proc/info/boot"),'user',input_username,input_password])
                else:
                    colors.show("su", "fail", input_username + ": wrong password.")
            else:
                colors.show("su", "fail", input_username + " user not found.")
        else:
            colors.show("su", "fail", input_username + " user not found.")

    # sudo command #
    def sudo (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == []:
            colors.show('sudo', 'fail', 'no inputs.')
            sys.exit(0)

        if not args[0].startswith('-'):

            ## Get user name ##

            thisuser = files.readall("/proc/info/su")

            ## Check guest account ##
            if thisuser == "guest":
                colors.show("sudo", 'fail', 'cannot use sudo command in guest user.')
                sys.exit(0)

            ## Check sudoers account ##
            if not thisuser == "root":
                sudoers = files.readall('/etc/sudoers')

                if not sudoers.__contains__(thisuser):
                    colors.show('sudo', 'fail', thisuser + ": user is'nt sudoers account.")
                    sys.exit()

            ## Send /etc/users/root to /proc/info/su username ##

            files.write("/proc/info/su", 'root')

            prompt = [sys.executable,files.readall('/proc/info/boot'), 'exec']

            for i in args:
                prompt.append(i)

            subprocess.call(prompt)

            files.write("/proc/info/su", thisuser)
        elif args[0] == '-a':
            ## Check root ##
            if not permissions.check_root(files.readall("/proc/info/su")):
                colors.show("sudo", "perm", "")
                sys.exit(0)
            ## Check user exists or no ##
            if files.isfile('/etc/users/' + args[1]):
                hashname = hashlib.sha3_256(args[1].encode()).hexdigest()
                username = control.read_record('username', '/etc/users/' + args[1])

                if hashname == username:
                    files.append('/etc/sudoers', args[1] + "\n")
                else:
                    colors.show('sudo', 'fail', args[1] + ": user not found.")
            else:
                colors.show('sudo', 'fail', args[1] + ": user not found.")
        else:
            colors.show('sudo', 'fail', args[1] + ": option not found.")

    # uadd command #
    def uadd (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == []:
            colors.show("uadd", "fail", "no inputs.")
            sys.exit(0)

        input_username = args[0]
        user = files.readall ("/proc/info/su")

        if permissions.check_root(user):
            ## Check exists user ##
            if files.isfile("/etc/users/" + input_username) or input_username == "root":
                colors.show("uadd", "fail", input_username + ": user exists.")
            elif input_username == "guest":
                colors.show("uadd", "fail", "cannot create user account with guest username.")
            else:
                while True:
                    password = getpass.getpass('Enter a new password: ')
                    confirm = getpass.getpass('Confirm the new password: ')
                    if password == confirm: break

                ## Informations ##
                first_name = input('\tFirst name      []: ')
                last_name =  input('\tLast name       []: ')
                company =    input('\tCompany name    []: ')
                birthday =   input('\tBirthday        []: ')
                gender =     input('\tGender          [Male/Female]: ')
                blood_type = input('\tBlood type      [O/A/B/AB]: ')
                phone =      input('\tPhone number    []: ')
                website =    input('\tWebsite address []: ')
                email =      input('\tEmail address   []: ')

                hashname = hashlib.sha3_256(str(input_username).encode()).hexdigest()
                hashcode = hashlib.sha3_512(str(password).encode()).hexdigest()

                files.create("/etc/users/" + input_username)
                control.write_record("username", hashname, '/etc/users/' + input_username)
                control.write_record("code", hashcode, '/etc/users/' + input_username)

                ## Add informations ##
                if not (first_name == None or first_name == ""):
                    control.write_record("first_name", first_name, '/etc/users/' + input_username)
                if not (last_name == None or last_name == ""):
                    control.write_record("last_name", last_name, '/etc/users/' + input_username)
                if not (company == None or company == ""):
                    control.write_record("company", company, '/etc/users/' + input_username)
                if not (birthday == None or birthday == ""):
                    control.write_record("birthday", birthday, '/etc/users/' + input_username)
                if not (gender == None or gender == ""):
                    control.write_record("gender", gender, '/etc/users/' + input_username)
                if not (blood_type == None or blood_type == ""):
                    control.write_record("blood_type", blood_type, '/etc/users/' + input_username)
                if not (phone == None or phone == ""):
                    control.write_record("phone", phone, '/etc/users/' + input_username)
                if not (website == None or website == ""):
                    control.write_record("website", website, '/etc/users/' + input_username)
                if not (email == None or email == ""):
                    control.write_record("email", email, '/etc/users/' + input_username)

                control.write_record('/desk/'+input_username,"drwxr-x---/"+input_username,'/etc/permtab')

        else:
            colors.show("uadd", "perm", "")

    # udel command #
    def udel (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if args == []:
            colors.show("udel", "fail", "no inputs.")
            sys.exit(0)

        input_username = args[0]
        user = files.readall ("/proc/info/su")

        if input_username == user:
            colors.show("udel", "fail", input_username + ": cannot remove switched user.")
        else:
            if permissions.check_root(user):
                if not files.isfile("/etc/users/" + input_username):
                    colors.show("udel", "fail", input_username + ": user not found.")
                else:
                    if input_username == "root":
                        colors.show("udel", "fail", input_username + ": is a permanet user.")
                    else:
                        hashname = hashlib.sha3_256(str(input_username).encode()).hexdigest()  ## Create hashname
                        username = control.read_record("username", "/etc/users/" + input_username)

                        if not hashname == username:
                            colors.show("udel", "fail", input_username + ": user not found.")
                        else:
                            files.remove("/etc/users/" + input_username)
                            if files.isdir('/desk/' + input_username):
                                files.removedirs("/desk/" + input_username)
                                control.remove_record('/desk/'+input_username,'/etc/permtab')
            else:
                colors.show("udel", "perm", "")

    # uinfo command #
    def uinfo (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        input_username = None

        if args == []:
            input_username = files.readall ("/proc/info/su")
        else:
            input_username = args[0]

        enable_cli = control.read_record("enable_cli", "/etc/guest")
        if not (input_username == "guest" and enable_cli == "Yes"):
            if files.isfile("/etc/users/" + input_username):
                ## Get information from user database ##
                first_name = control.read_record("first_name", "/etc/users/" + input_username)
                last_name = control.read_record("last_name", "/etc/users/" + input_username)
                company = control.read_record("company", "/etc/users/" + input_username)
                birthday = control.read_record("birthday", "/etc/users/" + input_username)
                gender = control.read_record("gender", "/etc/users/" + input_username)
                blood_type = control.read_record("blood_type", "/etc/users/" + input_username)
                phone = control.read_record("phone", "/etc/users/" + input_username)
                website = control.read_record("website", "/etc/users/" + input_username)
                email = control.read_record("email", "/etc/users/" + input_username)

                ## Show it on screen ##
                bold = colors.color(1, colors.get_bgcolor(), colors.get_fgcolor())
                if not (first_name == None or first_name == ""):  print(
                    "\t   First name: " + bold + first_name + colors.get_colors())
                if not (last_name == None or last_name == ""):    print(
                    "\t    Last name: " + bold + last_name + colors.get_colors())
                if not (company == None or company == ""):        print(
                    "\t      Company: " + bold + company + colors.get_colors())
                if not (birthday == None or birthday == ""):      print(
                    "\t     Birthday: " + bold + birthday + colors.get_colors())
                if not (gender == None or gender == ""):          print(
                    "\t       Gender: " + bold + gender + colors.get_colors())
                if not (blood_type == None or blood_type == ""):  print(
                    "\t    BloodType: " + bold + blood_type + colors.get_colors())
                if not (phone == None or phone == ""):            print(
                    "\t Phone number: " + bold + phone + colors.get_colors())
                if not (website == None or website == ""):        print(
                    "\t      Website: " + bold + website + colors.get_colors())
                if not (email == None or email == ""):            print(
                    "\tEmail address: " + bold + email + colors.get_colors())
            else:
                colors.show("uinfo", "fail", input_username + ": user not found.")

    # unsel command #
    def unsel (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        select = files.readall("/proc/info/sel")
        if select == "/proc/" + files.readall("/proc/info/sp"):
            colors.show("unsel", "warning", "controller has already selected.")
        else:
            files.write("/proc/info/sel", "/proc/" + files.readall("/proc/info/sp"))
            if files.isfile("/proc/selected"): files.remove("/proc/selected")

    # upv command #
    def upv (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        if not permissions.check_root(files.readall("/proc/info/su")):
            colors.show("upv", "perm", "")
            sys.exit(0)

        sel = files.readall('/proc/info/sel')  ## Get selector

        ## List all controls ##

        listc = control.read_list(sel)

        for i in listc:
            if not i.__contains__(':'):
                pass
            else:
                spliter = i.split(': ')
                files.write('/proc/info/' + spliter[0], spliter[1])

    # wget command #
    def wget (self,args):
        modules = Modules()
        files = Files()
        control = Control()
        colors = Colors()
        process = Process()
        permissions = Permissions()

        # https://www.tutorialspoint.com/downloading-files-from-web-using-python

        ## Check params ##

        if args == [] and args[1:]:
            colors.show('wget', 'fail', 'no inputs.')
            sys.exit(0)

        ## Download ##

        url = args[0]

        import requests
        r = requests.get(url, allow_redirects=True)
        ## Check permissions ##
        if permissions.check(files.output(args[1]), "w", files.readall("/proc/info/su")):
            open(files.input(args[1]), 'wb').write(r.content)
        else:
            colors.show("wget", "perm", "")


# package #
class Package:
    ## Clean the cache ##
    def clean (self):
        permissions = Permissions()
        files = Files()
        colors = Colors()

        if permissions.check_root(files.readall("/proc/info/su")):
            if files.isdir("/app/cache"):
                files.removedirs("/app/cache")
                files.mkdir("/app/cache")
                files.mkdir("/app/cache/gets")
                files.mkdir("/app/cache/archives")
                files.mkdir("/app/cache/archives/code")
                files.mkdir("/app/cache/archives/control")
                files.mkdir("/app/cache/archives/data")
                files.mkdir("/app/cache/archives/build")
        else:
            colors.show("paye", "perm", "")

    ## Create .pa archive ##

    def build(self,name):
        permissions = Permissions()
        files = Files()
        colors = Colors()

        if permissions.check_root(files.readall("/proc/info/su")):
            if not files.isfile(name + "/control/manifest"):
                colors.show("paye", "fail", "cannot create archive package")
                self.clean()
                sys.exit(0)

            if not files.isdir(name + "/data"): files.mkdir(name + "/data")
            if not files.isdir(name + "/code"): files.mkdir(name + "/code")

            ## Remove cache archives ##
            if files.isdir('/app/cache/archives/control'): files.removedirs('/app/cache/archives/control')
            if files.isdir('/app/cache/archives/data'): files.removedirs('/app/cache/archives/data')
            if files.isdir('/app/cache/archives/code'): files.removedirs('/app/cache/archives/code')

            ## Copy dir ##
            files.copydir(name + '/data', '/app/cache/archives/data')
            files.copydir(name + '/control', '/app/cache/archives/control')
            files.copydir(name + '/code', '/app/cache/archives/code')

            ## Pack archives ##
            shutil.make_archive(files.input("/app/cache/archives/build/data"), "zip",
                                files.input('/app/cache/archives/data'))
            shutil.make_archive(files.input("/app/cache/archives/build/control"), "zip",
                                files.input('/app/cache/archives/control'))
            shutil.make_archive(files.input("/app/cache/archives/build/code"), "zip",
                                files.input('/app/cache/archives/code'))
            shutil.make_archive(files.input(name), "zip", files.input("/app/cache/archives/build"))

            files.cut(name + ".zip", name + ".pa")
            ## Unlock the cache ##
        else:
            colors.show("paye", "perm", "")


    ## Unpack .pa archives ##

    def unpack(self,name):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control()
        commands = Commands()

        if permissions.check_root(files.readall("/proc/info/su")):
            ## unpack package ##
            shutil.unpack_archive(files.input(name), files.input("/app/cache/archives/build"), "zip")

            shutil.unpack_archive(files.input("/app/cache/archives/build/data.zip"),
                                  files.input("/app/cache/archives/data"), "zip")
            shutil.unpack_archive(files.input("/app/cache/archives/build/control.zip"),
                                  files.input("/app/cache/archives/control"), "zip")
            shutil.unpack_archive(files.input("/app/cache/archives/build/code.zip"),
                                  files.input("/app/cache/archives/code"), "zip")

            ## Get database of this package ##
            name = control.read_record("name", "/app/cache/archives/control/manifest").lower()
            unpack = control.read_record("unpack", "/app/cache/archives/control/manifest")
            depends = control.read_record("depends", "/app/cache/archives/control/manifest")

            if not (depends == None):
                depends.split(",")

            ## Search for tree dependency ##

            if not depends == None:
                for i in depends:
                    if not files.isfile("/app/packages/" + i + ".manifest"):
                        System ('paye -i ' + name)

            ## Write dependency ##

            if not depends == None:
                for i in depends:
                    files.create("/app/packages/" + i + ".depends")
                    files.write("/app/packages/" + i + ".depends", name + "\n")

            ## Run preinstall script ##

            if files.isfile('/app/cache/archives/control/preinstall.sa'):
                files.copy('/app/cache/archives/control/preinstall.sa', '/usr/app/preinstall.sa')
                System('preinstall')  # Run it
                files.remove('/usr/app/preinstall.sa')

                ## Copy preinstall script ##

                files.copy('/app/cache/archives/control/preinstall.sa', '/app/packages/' + name + ".preinstall")

            ## Setting up ##

            if files.isfile("/app/cache/archives/control/list"): files.copy("/app/cache/archives/control/list","/app/packages/" + name + ".list")
            if files.isfile("/app/cache/archives/control/manifest"): files.copy("/app/cache/archives/control/manifest","/app/packages/" + name + ".manifest")
            if files.isfile("/app/cache/archives/control/compile"): files.copy("/app/cache/archives/control/compile","/app/packages/" + name + ".compile")

            compilefiles = control.read_record('compile','/app/cache/archives/control/manifest')
            if compilefiles=='Yes':
                compiles = control.read_list('/app/cache/archives/control/compile')

                for i in compiles:
                    spl = i.split(":")

                    code = '/app/cache/archives/code/' + spl[0]
                    dest = "/app/cache/archives/data/" + spl[1]
                    commands.cc([code, dest])

            ## Create data archive ##
            shutil.make_archive(files.input("/app/cache/archives/build/data"), 'zip',files.input('/app/cache/archives/data'))

            ## Unpack data again ##
            shutil.unpack_archive(files.input("/app/cache/archives/build/data.zip"), files.input(unpack), "zip")

            ## Save the source

            shutil.unpack_archive(files.input('/app/cache/archives/build/code.zip'),files.input('/usr/src/'+name),'zip')

            ## After install ##

            ## Run postinstall script ##

            if files.isfile('/app/cache/archives/control/postinstall.sa'):
                files.copy('/app/cache/archives/control/postinstall.sa', '/usr/app/postinstall.sa')
                System('postinstall')  # Run it
                files.remove('/usr/app/postinstall.sa')

                ## Copy preinstall script ##

                files.copy('/app/cache/archives/control/postinstall.sa', '/app/packages/' + name + ".postinstall")

            ## Copy other scripts ##
            if files.isfile('/app/cache/archives/control/preremove.sa'):
                files.copy('/app/cache/archives/control/preremove.sa', '/app/packages/' + name + ".preremove")

            if files.isfile('/app/cache/archives/control/postremove.sa'):
                files.copy('/app/cache/archives/control/postremove.sa', '/app/packages/' + name + ".postremove")


            ## Unlock the cache ##
        else:
            colors.show("paye", "perm", "")

    ## Remove package ##
    def uninstall (self,name):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control ()
        name = name.lower()

        if permissions.check_root(files.readall("/proc/info/su")):

            location = "/app/packages/" + name + ".manifest"

            if not files.isfile(location):
                colors.show("paye", "fail", name + ": package not found")
                self.clean()
                sys.exit(0)

            ## Database control ##

            list = "/app/packages/" + name + ".list"
            compile = '/app/packages/'+name+".compile"
            preinstall = "/app/packages/" + name + ".preinstall"
            postinstall = "/app/packages/" + name + ".postinstall"
            preremove = "/app/packages/" + name + ".preremove"
            postremove = "/app/packages/" + name + ".postremove"
            depends = "/app/packages/" + name+ ".depends"

            ## Create preremove and postremove copies ##

            if files.isfile(preremove): files.copy(preremove, "/usr/app/preremove.sa")
            if files.isfile(postremove): files.copy(postremove, "/usr/app/postremove.sa")

            ## Run pre remove script ##

            if files.isfile ('/usr/app/preremove.sa'):
                System("preremove")
                files.remove('/usr/app/preremove.sa')

            ## Remove depends ##

            if files.isfile(depends):
                depends = control.read_list(depends)
                for i in depends:
                    self.remove(i)

            ####################

            unpack = control.read_record("unpack", location)

            ## Unpacked removal ##
            filelist = control.read_list(list)

            for i in filelist:
                if files.isdir(unpack + "/" + i):
                    files.removedirs(unpack + "/" + i)
                elif files.isfile(unpack + "/" + i):
                    files.remove(unpack + "/" + i)

            ## Database removal ##

            if files.isfile(location): files.remove(location)
            if files.isfile(list): files.remove(list)
            if files.isfile(preinstall): files.remove(preinstall)
            if files.isfile(postinstall): files.remove(postinstall)
            if files.isfile(preremove): files.remove(preremove)
            if files.isfile(postremove): files.remove(postremove)
            if files.isfile(depends): files.remove(depends)
            if files.isfile(compile): files.remove(compile)

            ## Remove the source code ##

            if files.isdir ('/usr/src/'+name): files.removedirs('/usr/src/'+name)

            ## Run postremove script ##

            if files.isfile ('/usr/app/postremove.sa'):
                System ("postremove")
                files.remove('/usr/app/postremove.sa')
        else:
            colors.show("paye", "perm", "")

    ## Download package ##

    def download(self,packname):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control()

        packname = packname.lower()

        if permissions.check_root(files.readall("/proc/info/su")):
            mirror = files.readall('/app/mirrors/' + packname)

            ## Download the file ##
            url = mirror

            import requests
            r = requests.get(url, allow_redirects=True)

            ## Check permissions ##
            open(files.input('/app/cache/gets/' + packname + '.pa'), 'wb').write(r.content)
        else:
            colors.show("paye", "perm", "")

    ## Create a mirro ##
    def add (self,mirror,name):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control()

        if permissions.check_root(files.readall("/proc/info/su")):
            endsplit = mirror.replace('https://', '').replace('http://', '')
            endsplit = mirror.split('/')
            files.write('/app/mirrors/' + name.replace('.pa',''), mirror)
        else:
            colors.show("paye", "perm", "")

    # update cloud software #
    def upcloud (self, mirror):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control()
        commands = Commands()

        if permissions.check_root(files.readall("/proc/info/su")):
            self.add('https://github.com/manijamali2003/pyabr/archive/master.zip','pyabr')
            self.download('pyabr')

            # backup #
            if files.isdir ('/app/cache/backups/users.bak.d'):
                files.copydir('/etc/users','/app/cache/backups/users.bak.d')

            if files.isfile ('/app/cache/backups/colors.bak'):
                files.copy('/etc/colors','/app/cache/backups/colors.bak')

            if files.isfile ('/app/cache/backups/compiler.bak'):
                files.copy('/etc/compiler','/app/cache/backups/compiler.bak')

            if files.isfile ('/app/cache/backups/exec.bak'):
                files.copy('/etc/exec','/app/cache/backups/exec.bak')

            if files.isfile ('/app/cache/backups/fstab.bak'):
                files.copy('/etc/fstab','/app/cache/backups/fstab.bak')

            if files.isfile ('/app/cache/backups/guest.bak'):
                files.copy('/etc/guest','/app/cache/backups/guest.bak')
                
            if files.isfile ('/app/cache/backups/gui.bak'):
                files.copy('/etc/gui','/app/cache/backups/gui.bak')
                
            if files.isfile ('/app/cache/backups/hostname.bak'):
                files.copy('/etc/hostname','/app/cache/backups/hostname.bak')
                
            if files.isfile ('/app/cache/backups/interface.bak'):
                files.copy('/etc/interface','/app/cache/backups/interface.bak')

            if files.isfile('/app/cache/backups/modules.bak'):
                files.copy('/etc/modules', '/app/cache/backups/modules.bak')
                
            if files.isfile ('/app/cache/backups/permtab.bak'):
                files.copy('/etc/permtab','/app/cache/backups/permtab.bak')

            if files.isfile('/app/cache/backups/time.bak'):
                files.copy('/etc/time', '/app/cache/backups/time.bak')

            # check version #
            now_version = control.read_record('version','/etc/distro')

            o0 = int(now_version.split('.')[0])
            o1 = int(now_version.split('.')[1])
            o2 = int(now_version.split('.')[2])

            ## unpack pyabr ##
            shutil.unpack_archive(files.input('/app/cache/gets/pyabr.pa'),files.input('/tmp'),'zip')

            ## Should be develop ... ##
            new_version = control.read_record('version','/tmp/pyabr-master/packs/pyabr/data/etc/distro')

            n0 = int(new_version.split('.')[0])
            n1 = int(new_version.split('.')[1])
            n2 = int(new_version.split('.')[2])

            # list upgrades internal packages #

            if o0<=n0 or o1<=n1 or o2<n2:
                listu = files.list('/app/packages')
                for i in listu:
                    if i.endswith('.manifest'):
                        if files.isdir('/tmp/pyabr-master/packs/' + i.replace('.manifest', '')):
                            self.build('/tmp/pyabr-master/packs/' + i.replace('.manifest', ''))
                            self.unpack('/tmp/pyabr-master/packs/' + i.replace('.manifest', '.pa'))
            else:
                colors.show ('paye','warning','all package was up to date.')
        else:
            colors.show("paye", "perm", "")
    ##  remove a mirror ##
    def remove (self,name):
        permissions = Permissions()
        files = Files()
        colors = Colors()
        control = Control()

        if permissions.check_root(files.readall("/proc/info/su")):
            files.remove('/app/mirrors/' + name)
        else:
            colors.show("paye", "perm", "")
# res #
class Res:
    def __init__(self):
        pass
    # get translated number #
    def num (self,number):
        control = Control()
        files = Files()
        number = str(number)

        locale = control.read_record('locale','/etc/gui')

        if not files.isfile('/usr/share/locales/'+locale+".locale"):
            locale = 'en'

        tnumber = ''
        for i in number:
            if i.isdigit():
                tnumber += i.replace(i,control.read_record(i,'/usr/share/locales/'+locale+".locale"))
            else:
                tnumber += i

        return tnumber

    # get resource #
    def get(self,filename):
        files = Files()
        control = Control()

        # Check Android #
        android = False
        if files.readall('/proc/info/os')=='Android': android=True

        if not filename == None:
            filename = filename.split("/")  # @widget:barge

            share = filename[0]
            name = filename[1]

            ## Real Resource ##
            if share.startswith("@layout"):
                if files.isfile("/usr/share/" + share.replace("@layout", "layouts") + "/" + name + ".ui"):
                    return files.input("/usr/share/" + share.replace("@layout", "layouts") + "/" + name + ".ui")
                else:
                    return None

            elif share.startswith("@font"):
                if files.isfile("/usr/share/fonts/" + name + ".ttf"):
                    return files.input("/usr/share/fonts/" + name + ".ttf")
                else:
                    return None

            elif share.startswith("@background"):
                if files.isfile("/usr/share/backgrounds/" + name + ".svg"):
                    if android==False:
                        return files.input(
                            "/usr/share/backgrounds/" + name + ".svg")
                    elif files.isfile("/usr/share/backgrounds/" + name + ".png"):
                        return files.input("/usr/share/backgrounds/" + name + ".png")
                elif files.isfile(
                        "/usr/share/backgrounds/" + name + ".png"):
                    return files.input(
                        "/usr/share/backgrounds/" + name + ".png")
                elif files.isfile(
                        "/usr/share/backgrounds/" + name + ".jpg"):
                    return files.input(
                        "/usr/share/backgrounds/" + name + ".jpg")
                elif files.isfile(
                        "/usr/share/backgrounds/" + name + ".jpeg"):
                    return files.input(
                        "/usr/share/backgrounds/" + name + ".jpeg")
                elif files.isfile(
                        "/usr/share/backgrounds/" + name + ".gif"):
                    return files.input(
                        "/usr/share/backgrounds/" + name + ".gif")
                else:
                    return None

            elif share.startswith("@image"):
                if files.isfile("/usr/share/images/" + name + ".svg"):
                    if android==False:
                        return files.input(
                        "/usr/share/images/" + name + ".svg")
                    elif files.isfile("/usr/share/images/" + name + ".png"):
                        return files.input("/usr/share/images/" + name + ".png")
                elif files.isfile(
                        "/usr/share/images/" + name + ".png"):
                    return files.input(
                        "/usr/share/images/" + name + ".png")
                elif files.isfile(
                        "/usr/share/images/" + name + ".jpg"):
                    return files.input(
                        "/usr/share/images/" + name + ".jpg")
                elif files.isfile(
                        "/usr/share/images/" + name + ".jpeg"):
                    return files.input(
                        "/usr/share/images/" + name + ".jpeg")
                elif files.isfile(
                        "/usr/share/images/" + name + ".gif"):
                    return files.input(
                        "/usr/share/images/" + name + ".gif")
                else:
                    return None

            elif share.startswith("@app"):
                if files.isfile("/usr/share/" + share.replace("@app", "applications") + "/" + name + ".desk"):
                    return files.input("/usr/share/" + share.replace("@app", "applications") + "/" + name + ".desk")
                else:
                    return None

            elif share.startswith("@widget"):
                if files.isfile("/usr/share/" + share.replace("@widget", "widgets") + "/" + name + ".desk"):
                    return files.input("/usr/share/" + share.replace("@widget", "widgets") + "/" + name + ".desk")
                else:
                    return None

            elif share.startswith("@shell"):
                if files.isfile("/usr/share/" + share.replace("@shell", "shells") + "/" + name + ".desk"):
                    return files.input("/usr/share/" + share.replace("@shell", "shells") + "/" + name + ".desk")
                else:
                    return None

            elif share.startswith("@icon"):
                if files.isfile("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".svg"):
                    if android==False:
                        return files.input("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".svg")
                    elif files.isfile("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".png"):
                        return files.input("/usr/share/icons/" + name + ".png")
                elif files.isfile("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".png"):
                    return files.input("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".png")
                elif files.isfile("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".gif"):
                    return files.input("/usr/share/" + share.replace("@icon", "icons") + "/" + name + ".gif")
                else:
                    return None

            elif share.startswith("@string"):
                locale = control.read_record("locale", "/etc/gui")
                id = files.readall("/proc/info/id")

                ## Set default lang ##
                if locale == None: locale = "en"

                ## Get value from string ##
                result = control.read_record(id.replace(".desk", "") + "." + name,
                                             "/usr/share/locales/" + locale + ".locale")

                ## Find default ##
                if result == None:
                    result = control.read_record(id.replace(".desk", "") + "." + name,
                                                 "/usr/share/locales/" + 'en' + ".locale")

                return result

            ## None Resource ##
            else:
                return None
        else:
            return None
# system #
class System:
    def __init__(self,cmd):
        files = Files()
        prompt = [sys.executable,files.readall("/proc/info/boot"), 'exec']
        cmdln = cmd.split(" ")

        if '' in cmdln:
            cmdln.remove('')

        for i in cmdln:
            prompt.append(i)

        subprocess.call(prompt)
# app #
class App:
    ## Start ID Process ##
    def start(self,id):
        files = Files()
        control = Control()
        colors = Colors()
        self.lang = control.read_record('locale', '/etc/gui')
        ## Check exists ##
        if files.isfile('/proc/id/' + id):
            pass


        ## Create id ##
        files.create("/proc/id/" + id)

        ## Check desktop shortcut ##
        if files.isfile("/usr/share/applications/" + id):
            files.copy("/usr/share/applications/" + id + ".desk",
                       "/proc/id/" + id)  # Copy all informations about this GUI application

        ## Set default id ##
        files.write("/proc/info/id", id)

    ## Check id ##
    def check(self,id):
        files = Files()
        control = Control()
        colors = Colors()
        self.lang = control.read_record('locale', '/etc/gui')
        if not files.isfile('/proc/id/' + id):
            return False
        else:
            return True

    ## End id ##
    def end(self,id):
        files = Files()
        control = Control()
        colors = Colors()
        self.lang = control.read_record('locale', '/etc/gui')
        if files.isfile('/proc/id/' + id):
            ## Remove id ##
            files.remove("/proc/id/" + id)

    ## Shut id ##
    def shut(self):
        files = Files()
        control = Control()
        colors = Colors()
        self.lang = control.read_record('locale', '/etc/gui')
        default = files.readall("/proc/info/id")
        if files.isfile("/proc/id/" + default):
            self.end(default)

    ## Endall id ##
    def endall(self):
        files = Files()
        control = Control()
        colors = Colors()
        self.lang = control.read_record('locale', '/etc/gui')
        self.switch('desktop')
        listid = files.list("/proc/id")
        for i in listid:
            if files.isfile('/proc/id/' + i):
                files.remove('/proc/id/' + i)

    ## Switch id process ##
    def switch(self,id):
        files = Files()
        control = Control()
        colors = Colors()
        self.lang = control.read_record('locale', '/etc/gui')
        if files.isfile('/proc/id/' + id):
            files.write("/proc/info/id", id)

    ## Check application ##
    def exists (self,app):
        files = Files()
        if files.isfile('/usr/share/applications/'+app+".desk"):
            return True
        else:
            return False

# process #

class Process:
    def __init__(self):
        pass
    def processor(self):
        files = Files()
        control = Control()
        colors = Colors()

        j = 0
        if not files.isfile("/proc/" + str(0)):
            files.create("/proc/" + str(0))
            j = j + 1
        else:
            list = files.list("/proc")
            list.remove('id')
            list.remove('info')

            for i in list:
                if files.isfile("/proc/" + i):

                    files.create("/proc/" + str(int(i) + 1))
                    j = j + 1
                else:
                    files.create("/proc/" + i)

        if files.isfile("/proc/1"):
            files.write("/proc/info/sp", str(j))
            return j
        else:
            files.write("/proc/info/sp", str(j - 1))
            return j - 1

    ## Check switched process ##
    def check(self,switch):
        files = Files()
        control = Control()
        colors = Colors()

        if not files.isfile("/proc/" + str(switch)):
            sys.exit(0)
        else:
            if files.isfile("/proc/info/sp"): files.remove("/proc/info/sp")
            files.write("/proc/info/sp", str(switch))

    ## End switched process ##
    def end(self,switch):
        files = Files()
        control = Control()
        colors = Colors()

        if files.isfile("/proc/info/sp"): files.remove("/proc/info/sp")
        if files.isfile("/proc/" + str(switch)):
            files.remove("/proc/" + str(switch))
            sys.exit(0)

    ## Endall all switched processes ##
    def endall(self):
        files = Files()
        control = Control()
        colors = Colors()

        if files.isfile("/proc/info/sp"): files.remove("/proc/info/sp")
        list = files.list("/proc")
        list.remove("id")
        list.remove("info")
        for i in list:
            files.remove("/proc/" + str(i))
# permissions #
class Permissions:
    def __init__(self):
        pass
    ## Create permissions ##
    def create(self,name, user, others, guest, owner):
        files = Files()
        control = Control()
        colors = Colors()

        if files.isfile(name) or files.isdir(name):
            ## Learned by Guru99 2020 ##
            ## Set user permissions section
            if user == 0:
                user = "---"
            elif user == 1:
                user = "--x"
            elif user == 2:
                user = "-w-"
            elif user == 3:
                user = "-wx"
            elif user == 4:
                user = "r--"
            elif user == 5:
                user = "r-x"
            elif user == 6:
                user = "rw-"
            elif user == 7:
                user = "rwx"
            else:
                user = "rwx"

            ## Set other users permissions section
            if others == 0:
                others = "---"
            elif others == 1:
                others = "--x"
            elif others == 2:
                others = "-w-"
            elif others == 3:
                others = "-wx"
            elif others == 4:
                others = "r--"
            elif others == 5:
                others = "r-x"
            elif others == 6:
                others = "rw-"
            elif others == 7:
                others = "rwx"
            else:
                others = "rwx"

            ## Set guest user permissions section
            if guest == 0:
                guest = "---"
            elif guest == 1:
                guest = "--x"
            elif guest == 2:
                guest = "-w-"
            elif guest == 3:
                guest = "-wx"
            elif guest == 4:
                guest = "r--"
            elif guest == 5:
                guest = "r-x"
            elif guest == 6:
                guest = "rw-"
            elif guest == 7:
                guest = "rwx"
            else:
                guest = "rwx"

            if files.isdir(name):
                control.write_record(name, "d" + user + others + guest + "/" + owner,
                                     "/etc/permtab")  # Write permissions for this directory
            else:
                control.write_record(name, "-" + user + others + guest + "/" + owner,
                                     "/etc/permtab")  # Write permissions for this file

    def exists(self,name):
        files = Files()
        control = Control()
        colors = Colors()

        perms = control.read_record(name, "/etc/permtab")  ## get permissions
        if perms == None:
            return False
        else:
            return True

    ## This function e.g. drwxrwxrwx/root --> 777 ##
    def show_number(self,perm):
        files = Files()
        control = Control()
        colors = Colors()

        perm = perm.split("/")
        owner = perm[1]
        perms = perm[0]

        dirfile = perms[0]
        user_r = perms[1]
        user_w = perms[2]
        user_x = perms[3]
        others_r = perms[4]
        others_w = perms[5]
        others_x = perms[6]
        guest_r = perms[7]
        guest_w = perms[8]
        guest_x = perms[9]

        user = user_r + user_w + user_x
        others = others_r + others_w + others_x
        guest = guest_r + guest_w + guest_x

        if user == '---':
            user = 0
        elif user == '--x':
            user = 1
        elif user == '-w-':
            user = 2
        elif user == '-wx':
            user = 3
        elif user == 'r--':
            user = 4
        elif user == 'r-x':
            user = 5
        elif user == 'rw-':
            user = 6
        elif user == 'rwx':
            user = 7

        if others == '---':
            others = 0
        elif others == '--x':
            others = 1
        elif others == '-w-':
            others = 2
        elif others == '-wx':
            others = 3
        elif others == 'r--':
            others = 4
        elif others == 'r-x':
            others = 5
        elif others == 'rw-':
            others = 6
        elif others == 'rwx':
            others = 7

        if guest == '---':
            guest = 0
        elif guest == '--x':
            guest = 1
        elif guest == '-w-':
            guest = 2
        elif guest == '-wx':
            guest = 3
        elif guest == 'r--':
            guest = 4
        elif guest == 'r-x':
            guest = 5
        elif guest == 'rw-':
            guest = 6
        elif guest == 'rwx':
            guest = 7

        strnum = str(user) + str(others) + str(guest)  # e.g. 7, 7, 7 --> "777"
        num = int(strnum)  # e.g. "777"-> 777

        return num

    ## This function correct at all ##
    def get_permissions(self,name):
        files = Files()
        control = Control()
        colors = Colors()

        perms = control.read_record(name, "/etc/permtab")  ## get permissions
        if not perms == None:
            return perms
        else:
            ## Father permtab ##
            if files.isdir(name):
                dirfile = "d"
            else:
                dirfile = "-"

            ## The most important part of father permtab ##
            names = name.split("/")

            while not self.exists(name):
                l = len(names) - 1
                names.pop(l)
                name = ""
                for i in names:
                    name = name + "/" + i
                name = name.replace("//", "/")

            perm = control.read_record(name, "/etc/permtab")  ## get permissions
            perm = perm.split("/")
            owner = perm[1]
            perms = perm[0]
            user_r = perms[1]
            user_w = perms[2]
            user_x = perms[3]
            others_r = perms[4]
            others_w = perms[5]
            others_x = perms[6]
            guest_r = perms[7]
            guest_w = perms[8]
            guest_x = perms[9]
            return dirfile + user_r + user_w + user_x + others_r + others_w + others_x + guest_r + guest_w + guest_x + "/" + owner

    ## This function correct at all ##
    def check(self,name, request, user):
        files = Files()
        control = Control()
        colors = Colors()

        perm = self.get_permissions(name)
        perm = perm.split("/")

        perms = perm[0]
        owner = perm[1]

        dirfile = perms[0]
        user_r = perms[1]
        user_w = perms[2]
        user_x = perms[3]
        others_r = perms[4]
        others_w = perms[5]
        others_x = perms[6]
        guest_r = perms[7]
        guest_w = perms[8]
        guest_x = perms[9]

        if user == "root":
            ## Check exists user ##
            if files.isfile("/etc/users/" + user):
                hashname = hashlib.sha3_256(str("root").encode()).hexdigest()
                username = control.read_record("username", "/etc/users/root")
                if (hashname == username):
                    return True
                else:
                    return False
            else:
                return False
        elif user == "guest":
            enable_cli = control.read_record("enable_cli", "/etc/guest")
            if enable_cli == "Yes":
                if owner == user:
                    if request == "r":
                        r = user_r
                        if r == "r":
                            return True
                        else:
                            return False
                    elif request == "w":
                        w = user_w
                        if w == "w":
                            return True
                        else:
                            return False
                    elif request == "x":
                        x = user_x
                        if x == "x":
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    if request == "r":
                        r = guest_r
                        if r == "r":
                            return True
                        else:
                            return False
                    elif request == "w":
                        w = guest_w
                        if w == "w":
                            return True
                        else:
                            return False
                    elif request == "x":
                        x = guest_x
                        if x == "x":
                            return True
                        else:
                            return False
                    else:
                        return False
            else:
                return False
        else:
            ## Check exists user ##
            if files.isfile("/etc/users/" + user):
                hashname = hashlib.sha3_256(str(user).encode()).hexdigest()
                username = control.read_record("username", "/etc/users/" + user)
                if (hashname == username):
                    if owner == user:
                        if request == "r":
                            r = user_r
                            if r == "r":
                                return True
                            else:
                                return False
                        elif request == "w":
                            w = user_w
                            if w == "w":
                                return True
                            else:
                                return False
                        elif request == "x":
                            x = user_x
                            if x == "x":
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        if request == "r":
                            r = others_r
                            if r == "r":
                                return True
                            else:
                                return False
                        elif request == "w":
                            w = others_w
                            if w == "w":
                                return True
                            else:
                                return False
                        elif request == "x":
                            x = others_x
                            if x == "x":
                                return True
                            else:
                                return False
                        else:
                            return False
                else:
                    return False
            else:
                return False

    ## Get owner ##
    def get_owner(self,filename):
        perm = self.get_permissions(filename)

        perm = perm.split("/")
        return perm[1]

    ## Check owner ##
    def check_owner(self,filename, user):
        files = Files()
        control = Control()
        colors = Colors()

        owner = self.get_owner(filename)
        if user == "guest":
            enable_cli = control.read_record("enable_cli", "/etc/guest")
            if enable_cli == "Yes":
                if owner == user:
                    return True
                else:
                    return False
            else:
                return False
        elif user == "root":
            if files.isfile("/etc/users/" + user):
                hashname = hashlib.sha3_256(str(user).encode()).hexdigest()
                username = control.read_record("username", "/etc/users/" + user)
                if (hashname == username):
                    return True
                else:
                    return False
            else:
                return False
        else:
            if files.isfile("/etc/users/" + user):
                hashname = hashlib.sha3_256(str(user).encode()).hexdigest()
                username = control.read_record("username", "/etc/users/" + user)
                if (hashname == username):
                    if owner == user:
                        return True
                    elif owner == "guest":
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    ## Check root ##
    def check_root(self,user):
        files = Files()
        control = Control()
        colors = Colors()

        if user == "root":
            if files.isfile("/etc/users/" + user):
                hashname = hashlib.sha3_256(str(user).encode()).hexdigest()
                username = control.read_record("username", "/etc/users/" + user)
                if (hashname == username):
                    return True
                else:
                    return False
            else:
                return False
# modules #
class Modules:
    def __init__(self):
        pass
    def get_modules(self):

        file = open("etc/modules")
        strv = file.read()
        file.close()
        strv = strv.split("\n")
        for i in strv:
            sys.path.append("./" + i)

    ## Import module ##
    def run_module(self,module):
        ## split ##
        m = module.split('/')
        m.pop(0)

        strv = ''

        for i in m:
            strv += i

        importlib.import_module(strv)

# files #
class Files:
    def __init__(self):
        pass

    root = "./"

    def input(self,filename):
        if filename.startswith("/"):
            return self.root + filename
        else:
            pwd = self.readall("/proc/info/pwd")
            return self.root + pwd + "/" + filename

    def output_shell(self,filename):
        return self.input(filename).replace("///", "/").replace("//", "/").replace("./", "/")

    def input_exec(self,filename):
        return self.input(filename.replace("./", "")).replace(".//", "").replace("/", ".")

    def output(self,filename):
        if filename.startswith("/"):
            return filename
        else:
            return self.input(filename).replace("///", "/").replace("//", "/").replace("./", "/").replace("//", "/")

    def create(self,filename):
        file = open(self.input(filename), "w")
        file.close()

    def readall(self,filename):
        file = open(self.input(filename), "r",encoding='utf-8')
        strv = file.read()
        file.close()
        return strv

    def write(self,filename, text):
        file = open(self.input(filename), "w")
        file.write(text)
        file.close()

    def append(self,filename, text):
        file = open(self.input(filename), "a")
        file.write(text)
        file.close()

    def isfile(self,filename):
        if os.path.isfile(self.input(filename)):
            return True
        else:
            return False

    def isdir(self,dirname):
        if os.path.isdir(self.input(dirname)):
            return True
        else:
            return False

    def mkdir(self,dirname):
        os.mkdir(self.input(dirname))

    def makedirs(self,dirname):
        os.makedirs(self.input(dirname))

    def remove(self,filename):
        os.remove(self.input(filename))

    def rmdir(self,dirname):
        os.rmdir(self.input(dirname))

    def removedirs(self,dirname):
        shutil.rmtree(self.input(dirname))

    def copy(self,src, dest):
        shutil.copyfile(self.input(src), self.input(dest))

    def cut(self,src, dest):
        self.copy(src, dest)
        self.remove(src)

    def copydir(self,src, dest):
        shutil.copytree(self.input(src), self.input(dest))

    def cutdir(self,src, dest):
        self.copydir(self.input(src), self.input(dest))
        self.removedirs(src)

    def list(self,path):
        return os.listdir(self.input(path))

    def parentdir(self,filename):
        file = self.input(filename)  ## Get file name

        file = file.split('/')
        file.pop(len(file) - 1)

        strv = ''
        for i in file:
            strv += i

        return strv

    def filename(self,path):
        file = self.input(path)  ## Get file name

        file = file.split('/')

        return file[len(file) - 1]
# control #
class Control:
    def __init__(self):
        pass
    def read_record(self,name, filename):
        files = Files()
        strv = files.readall(filename)
        strv = strv.split("\n")

        for i in strv:
            if i.startswith(name):
                i = i.split(": ")
                if i[0] == (name):
                    return i[1]

    def read_list(self,filename):
        files = Files()
        strv = files.readall(filename)
        strv = strv.split("\n")
        return strv

    def write_record(self,name, value, filename):
        files = Files()
        all = files.readall(filename)
        record = self.read_record(name, filename)
        files.remove(filename)
        if not (record == None):
            all = all.replace(name + ": " + record, "")
        files.write(filename, all + "\n" + name + ": " + value)

    def remove_record(self,name, filename):
        files = Files()
        all = files.readall(filename)
        record = self.read_record(name, filename)
        files.remove(filename)
        if not (record == None):
            all = all.replace(name + ": " + record, "")
        files.write(filename, all)

    def remove_item(self,name, filename):
        files = Files()
        items = self.read_list(filename)
        strv = ""
        for i in items:
            if i == name:
                strv = strv + "\n"
            else:
                strv = strv + "\n" + i
        files.write(filename, strv)

# colors #
class Colors:
    files = Files()
    control = Control()
    def __init__(self):
        pass
    argv = 'kernel'

    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    purple = 35
    cyan = 36
    white = 37

    style_none = 0
    style_bold = 1
    style_underline = 2
    style_negative1 = 3
    style_negative2 = 5

    bg_black = 40
    bg_red = 41
    bg_green = 42
    bg_yellow = 43
    bg_blue = 44
    bg_purple = 45
    bg_cyan = 46
    bg_white = 47

    def show(self,process_name, process_type, process_message):
        files = Files()
        control = Control()
        if process_type == "fail":
            print(self.get_fail() + process_name + ": error: " + process_message + self.get_colors())
        elif process_type == "perm":
            print(self.get_fail() + process_name + ": error: " + "Permission denied." + self.get_colors())
        elif process_type == "warning":
            print(self.get_warning() + process_name + ": warning: " + process_message + self.get_colors())
        elif process_type == "fail-start":
            print("[ " + self.get_fail() + "FAIL " + self.get_colors() + "] Fail to start " + process_name + " process.")
        elif process_type == "fail-switch":
            print("[ " + self.get_fail() + "FAIL " + self.get_colors() + "] Fail to switch " + process_name + " process.")
        elif process_type == "stop":
            print("[ " + self.get_fail() + "STOP" + self.get_colors() + " ] Stop the " + process_name)
        elif process_type == "fail-show":
            print("[ " + self.get_fail() + "FAIL" + self.get_colors() + " ] " + process_message)

    def color(self,style, text, background):
        files = Files()
        if not files.isfile("/proc/id/desktop"):
            return "\033[" + str(style) + ";" + str(text) + ";" + str(background) + "m"
        else:
            return ""

    def get_colors(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            fgcolor = control.read_record("fgcolor", "/etc/color")
            bgcolor = control.read_record("bgcolor", "/etc/color")
            style = control.read_record("style", "/etc/color")
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""

    def get_style(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("style", "/etc/color")
            return style
        else:
            return ""

    def get_fgcolor(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            fgcolor = control.read_record("fgcolor", "/etc/color")
            return fgcolor
        else:
            return ""

    def get_bgcolor(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            bgcolor = control.read_record("bgcolor", "/etc/color")
            return bgcolor
        else:
            return ""

    def get_warning(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("warning_style", "/etc/color")
            fgcolor = control.read_record("warning_fgcolor", "/etc/color")
            bgcolor = control.read_record("warning_bgcolor", "/etc/color")
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""

    def get_path(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("path_style", "/etc/color")
            fgcolor = control.read_record("path_fgcolor", "/etc/color")
            bgcolor = control.read_record("path_bgcolor", "/etc/color")
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""

    def get_prompt(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("prompt_style", "/etc/color")
            fgcolor = control.read_record("prompt_fgcolor", "/etc/color")
            bgcolor = control.read_record("prompt_bgcolor", "/etc/color")
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""

    def get_fail(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("fail_style", "/etc/color")
            fgcolor = control.read_record("fail_fgcolor", "/etc/color")
            bgcolor = control.read_record("fail_bgcolor", "/etc/color")
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""

    def get_ok(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("ok_style", "/etc/color")
            fgcolor = control.read_record("ok_fgcolor", "/etc/color")
            bgcolor = control.read_record("ok_bgcolor", "/etc/color")
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""

    def get_hide(self):
        files = Files()
        control = Control()
        if not files.isfile("/proc/id/desktop"):
            style = control.read_record("style", "/etc/color")
            bgcolor = control.read_record("bgcolor", "/etc/color")
            fgcolor = int(control.read_record("bgcolor", "/etc/color")) + 10
            strv = "\033[" + str(style) + ";" + str(fgcolor) + ";" + str(bgcolor) + "m"
            return strv
        else:
            return ""