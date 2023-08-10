import sys
from PyQt4 import QtGui
import Interfaces.MainScreen as MainScreen

app = QtGui.QApplication(sys.argv)
mainScreen = MainScreen.Screen()
mainScreen.showMaximized()
sys.exit(app.exec_())