"""
    Rachel's Setup

    Written by -> Mani Jamali
    github.com/manijamali2003
"""

# Import PyQt libs
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

# Import other libs
import sys, platform, py_compile as pyc, shutil, os
from pathlib import Path
import sqlite3

# Import PyAbr libs
from buildlibs import control, pack_archives as pack


# Support in Pyabr and other os
class MainApp(QWizard):
    def BrowseClick(self):
        self.leLocation.setText((QFileDialog().getExistingDirectory()))

    def Finish(self):
        connection = sqlite3.connect("packs/rachel/data/etc/rachel.db")
        cursor = connection.cursor()

        create_table_query = "CREATE TABLE userdata (username TEXT, firstname TEXT, lastname TEXT, email TEXT, phone TEXT, location TEXT)"

        cursor.execute(create_table_query)

        connection.commit()

        # Get all configure information
        if not (
                self.leLocation.text() is None and
                self.leUsername.text() is None and
                self.leFirstName.text() is None and
                self.leLastName.text() is None and
                self.leEmail.text() is None and
                self.lePhone.text() is None and
                self.chpath.currentText() is None and
                self.chds.currentText() is None
        ):
            location = self.leLocation.text()
            username = self.leUsername.text()
            firstname = self.leFirstName.text()
            lastname = self.leLastName.text()
            email = self.leEmail.text()
            phone = self.lePhone.text()

            if self.chpath.isChecked():
                file = open('/usr/bin/Rachel', 'w')
                file.write('cd ' + location + ' && {0} rachel.pyc'.replace('{0}', sys.executable))
                file.close()

                os.system('chmod +x /usr/bin/Rachel')

            # Write Data
            insert_user_data_query = f"INSERT INTO userdata (username, firstname, lastname, email, phone, location) VALUES ('{username}', '{firstname}', '{lastname}', '{email}', '{phone}', '{location}')"
            cursor.execute(insert_user_data_query)
            connection.commit()

            # Create compile files

            # Pre build
            if os.path.isdir("stor"):
                shutil.rmtree("stor")

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

            if not os.path.isdir("build-packs"):
                os.mkdir("build-packs")

            pack.install()
            shutil.copyfile('stor/usr/app/rachel.pyc', 'stor/rachel.pyc')

            shutil.make_archive('rachel', 'zip', 'stor')

            # Clean
            if os.path.isdir('app'):
                shutil.rmtree('app')
            if os.path.isdir('build-packs'):
                shutil.rmtree('build-packs')
            if os.path.isdir('stor'):
                shutil.rmtree('stor')

            # Unpack archive
            shutil.unpack_archive('rachel.zip', self.leLocation.text(), 'zip')

            if os.path.isfile('rachel.zip'):
                os.remove('rachel.zip')

    def __init__(self, ports):
        super(MainApp, self).__init__()

        # Ports used in pyabr
        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        # UI Setting up
        uic.loadUi('buildlibs/ui/setup.ui', self)

        # Find all objects
        self.leLocation = self.findChild(QLineEdit, 'leLocation')
        self.chpath = self.findChild(QCheckBox, 'chpath')
        self.chds = self.findChild(QCheckBox, 'chds')
        self.btnLocation = self.findChild(QPushButton, 'btnLocation')
        self.leFirstName = self.findChild(QLineEdit, 'leFirstName')
        self.leLastName = self.findChild(QLineEdit, 'leLastName')
        self.leUsername = self.findChild(QLineEdit, 'leUsername')
        self.leEmail = self.findChild(QLineEdit, 'leEmail')
        self.lePhone = self.findChild(QLineEdit, 'lePhone')

        self.button(QWizard.FinishButton).clicked.connect(self.Finish)

        self.btnLocation.clicked.connect(self.BrowseClick)

        pyabr_inst = str(Path.home())

        # Default location to install
        if platform.system() == "Windows":
            self.leLocation.setText(pyabr_inst + "\\Rachel")
        else:
            self.leLocation.setText(pyabr_inst + "/Rachel")

        # Show the setup page
        self.show()


app = QApplication(sys.argv)
w = MainApp([None, None, None, None, None])
sys.exit(app.exec())
