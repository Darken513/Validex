import matplotlib.pyplot as plt
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class MatplotlibWidget(QtGui.QWidget):
    def __init__(self, dataDict):
        super(MatplotlibWidget, self).__init__()
        # to do : make it responsive 
        self.listX = dataDict["listX"]
        self.listY = dataDict["listY"]
        self.slope = dataDict["slope"]
        self.intercept = dataDict["intercept"]

        # Create a Matplotlib figure and axes
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.axes.set_title('Matplotlib Graph')
        
        # plot the entered points by the user
        self.axes.plot(self.listX, self.listY, marker='o', linestyle='', color='red')

        gap = max(self.listX) - min(self.listX)
        lowX = min(self.listX) - gap/10
        highX = max(self.listX) + gap/10
        regression_x = np.linspace(0 if lowX<0 else lowX, highX, 100)
        regression_y = [ self.intercept + self.slope*number for number in regression_x ]

        # plot the line we think its best
        self.axes.plot(regression_x, regression_y)

        # Create a FigureCanvas widget
        self.canvas = FigureCanvas(self.figure)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.canvas)