import sys
from PyQt4 import QtGui
import Interfaces.MainScreen as MainScreen

app = QtGui.QApplication(sys.argv)
mainScreen = MainScreen.Screen()
mainScreen.showMaximized()
sys.exit(app.exec_())

""" import csv

data = [
    ["Name", "Age", "Location"],
    ["Achraf", 25, "Paris"],
    ["John", 30, "New York"],
    ["Alice", 28, "London"]
]

with open('data.csv', 'wb') as file:
    writer = csv.writer(file)
    writer.writerows(data) """