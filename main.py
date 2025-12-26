#! /usr/bin/env python 

from PyQt6.QtWidgets import QApplication
import sys

from UI.main import Gui

if __name__=="__main__":
     app = QApplication(sys.argv)
     gui=Gui()
     #gui.splashscreen()
     gui.show()
     app.exec()