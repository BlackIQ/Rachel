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

import shutil, os, sys, glob, platform, py_compile
from buildlibs import control


def compile(src, dest):
    py_compile.compile(src, dest)


# Build
def build(name):
    if not ("packs/" + name + "/code") and ("packs/" + name + "/data") and (
            "packs/" + name + "/control") and ("packs/" + name + "/control/manifest"):
        exit(0)

    shutil.make_archive("app/cache/archives/build/data", "zip", "packs/" + name + "/data")
    shutil.make_archive("app/cache/archives/build/code", "zip", "packs/" + name + "/code")
    shutil.make_archive("app/cache/archives/build/control", "zip", "packs/" + name + "/control")

    shutil.make_archive(name, "zip", "app/cache/archives/build")
    os.rename(name + ".zip", "build-packs/" + name + ".pa")
    clean()


# Clean the cache
def clean():
    shutil.rmtree("app/cache")
    os.mkdir("app/cache")
    os.mkdir("app/cache/gets")
    os.mkdir("app/cache/archives")
    os.mkdir("app/cache/archives/code")
    os.mkdir("app/cache/archives/control")
    os.mkdir("app/cache/archives/data")
    os.mkdir("app/cache/archives/build")


# Unpack .pa archives

def unpack(name):
    shutil.unpack_archive("build-packs/" + name + ".pa", "app/cache/archives/build", "zip")
    shutil.unpack_archive("app/cache/archives/build/data.zip", "app/cache/archives/data", "zip")
    shutil.unpack_archive("app/cache/archives/build/code.zip", "app/cache/archives/code", "zip")
    shutil.unpack_archive("app/cache/archives/build/control.zip", "app/cache/archives/control", "zip")

    # Unpack database only

    name = control.read_record("name", "app/cache/archives/control/manifest")
    unpack = control.read_record("unpack", "app/cache/archives/control/manifest")

    # Setting up

    if os.path.isfile("app/cache/archives/control/manifest"):
        shutil.copyfile("app/cache/archives/control/manifest", "stor/app/packages/" + name + ".manifest")
    if os.path.isfile("app/cache/archives/control/list"):
        shutil.copyfile("app/cache/archives/control/list", "stor/app/packages/" + name + ".list")
    if os.path.isfile("app/cache/archives/control/compile"):
        shutil.copyfile("app/cache/archives/control/compile", "stor/app/packages/" + name + ".compile")

    # Compile codes
    if os.path.isfile("app/cache/archives/control/compile"):
        listcodes = control.read_list("app/cache/archives/control/compile")
        for i in listcodes:
            i = i.split(":")

            compile('app/cache/archives/code/' + i[0], 'app/cache/archives/data/' + i[1])

    # Archive data again
    shutil.make_archive("app/cache/archives/build/data", "zip", "app/cache/archives/data")

    # Unpack data again
    shutil.unpack_archive("app/cache/archives/build/data.zip", "stor/" + unpack, "zip")

    # Save source code
    shutil.unpack_archive('app/cache/archives/build/code.zip', 'stor/usr/src/' + name, 'zip')
    clean()


def install():
    list = os.listdir('packs')
    for i in list:
        if os.path.isdir('packs/' + i):
            build(i)
            unpack(i)


def inst(pack):
    build(pack)
    unpack(pack)
