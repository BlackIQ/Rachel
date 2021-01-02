# Test !

from buildlibs import  control, pack_archives as pack
import os,shutil,subprocess as sub,sys

## Write Datas ##
control.write_record('username',control.read_record('username','debug.db'),'packs/rachel/data/etc/rachel')
control.write_record('firstname',control.read_record('firstname','debug.db'), 'packs/rachel/data/etc/rachel')
control.write_record('lastname', control.read_record('lastname','debug.db'), 'packs/rachel/data/etc/rachel')
control.write_record('email', control.read_record('email','debug.db'), 'packs/rachel/data/etc/rachel')
control.write_record('phone',control.read_record('phone','debug.db'), 'packs/rachel/data/etc/rachel')

            ## create compile files ##
            ## pre build ##
if os.path.isdir("stor"): shutil.rmtree("stor")

if not os.path.isdir("app"):
    os.mkdir("app")
    os.mkdir("app/cache")
    os.mkdir("app/cache/archives")
    os.mkdir("app/cache/archives/data")
    os.mkdir("app/cache/archives/control")
    os.mkdir("app/cache/archives/code")
    os.mkdir("app/cache/archives/build")
    os.mkdir("app/cache/gets")

if not os.path.isdir("stor"):
    os.mkdir("stor")
    os.mkdir("stor/app")
    os.mkdir("stor/app/packages")

if not os.path.isdir("build-packs"): os.mkdir("build-packs")

pack.install()
shutil.copyfile('stor/usr/app/rachel.pyc','stor/rachel.pyc')
os.system('cd stor && "'+sys.executable+'" rachel.pyc')
            # clean #
if os.path.isdir('app'): shutil.rmtree('app')
if os.path.isdir('build-packs'): shutil.rmtree('build-packs')
if os.path.isdir('stor'): shutil.rmtree('stor')
