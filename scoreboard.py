# -*- coding: utf-8 -*-
# __author__ = 'lidong'

"""
Description:
"""

from mainwindow import Mainwindow
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)
mywindows = Mainwindow()

mywindows.show()
sys.exit(app.exec_())