"""
    Rachel's Setup

    Written by -> Mani Jamali
    github.com/manijamali2003

    Rachel's Version -> 0.0.1
    Setup's  Version -> 0.0.1
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys , platform
from pathlib import Path
from pyabr_extensions import control

## Support in Pyabr and other os ##
class MainApp (QWizard):
    def BrowseClick(self):
        self.leLocation.setText((QFileDialog().getExistingDirectory()))

    def Finish(self):
        ## Get all configure information ##
        if not (
                self.leLocation.text() == None and
                self.leUsername.text() == None and
                self.leFirstName.text() == None and
                self.leLastName.text() == None and
                self.leEmail.text() == None and
                self.lePhone.text() == None and
                self.chpath.currentText() == None and
                self.chds.currentText() == None
        ):
            location = self.leLocation.text()
            username = self.leUsername.text()
            firstname = self.leFirstName.text()
            lastname = self.leLastName.text()
            email = self.leEmail.text()
            phone = self.lePhone.text()

            if self.chds.isChecked():
                desktop_shortcut = True
            else:
                desktop_shortcut = False

            if self.chpath.isChecked():
                add_to_path = True
            else:
                add_to_path = False

            ## Write Datas ##
            control.write_record('username',username,'database')
            control.write_record('firstname', firstname, 'database')
            control.write_record('lastname', lastname, 'database')
            control.write_record('email', email, 'database')
            control.write_record('phone', phone, 'database')

    def __init__(self,ports):
        super(MainApp, self).__init__()

        ## ports used in pyabr ##
        self.Backend = ports[0]
        self.Env = ports[1]
        self.Widget = ports[2]
        self.AppName = ports[3]
        self.External = ports[4]

        ## UI Setting up ##
        uic.loadUi('etc/setup.ui',self)

        ## Find all objects ##
        self.leLocation = self.findChild(QLineEdit, 'leLocation')
        self.chpath = self.findChild(QCheckBox, 'chpath')
        self.chds = self.findChild(QCheckBox,'chds')
        self.btnLocation = self.findChild(QPushButton,'btnLocation')
        self.leFirstName = self.findChild(QLineEdit,'leFirstName')
        self.leLastName = self.findChild(QLineEdit,'leLastName')
        self.leUsername = self.findChild(QLineEdit,'leUsername')
        self.leEmail = self.findChild(QLineEdit,'leEmail')
        self.lePhone = self.findChild(QLineEdit,'lePhone')

        self.button(QWizard.FinishButton).clicked.connect(self.Finish)

        self.btnLocation.clicked.connect(self.BrowseClick)

        pyabr_inst = str(Path.home())

        ## Default location to install ##
        if platform.system() == "Windows":
            self.leLocation.setText(pyabr_inst + "\\Rachel")
        else:
            self.leLocation.setText(pyabr_inst + "/Rachel")

        ## show the setup page ##
        self.show()

app = QApplication(sys.argv)
w = MainApp([None,None,None,None,None])
sys.exit(app.exec())