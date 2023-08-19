import matplotlib.pyplot as plt
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class MatplotlibWidget(QtGui.QWidget):
    def __init__(self, dataDict, isMultiChart):
        super(MatplotlibWidget, self).__init__()
        if(not isMultiChart):
            self.drawSingleChart(dataDict)
        else:
            self.drawMultiChart(dataDict, isMultiChart)
            
    def drawSingleChart(self, dataDict):
        # to do : make it responsive 
        self.listX = dataDict["listX"]
        self.listY = dataDict["listY"]
        self.slope = dataDict["slope"]
        self.r_value = dataDict["r_value"]
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

        # Add text annotations next to the chart
        equation = str(round(self.intercept, 3))+" + "+str(round(self.slope, 3))+" . X"
        self.axes.text(1.02, 0.9, "The equation : ", transform=self.axes.transAxes, fontsize=12, color='red')
        self.axes.text(1.02, 0.84, equation, transform=self.axes.transAxes, fontsize=12, color='red')
        self.axes.text(1.02, 0.72, 'Slope :' + str(round(self.slope, 6)), transform=self.axes.transAxes, fontsize=12, color='blue')
        self.axes.text(1.02, 0.60, 'Intercept :' + str(round(self.intercept, 6)), transform=self.axes.transAxes, fontsize=12, color='green')
        self.axes.text(1.02, 0.48, 'Correlation coefficient :', transform=self.axes.transAxes, fontsize=12, color='grey')
        self.axes.text(1.02, 0.42, str(round(self.r_value, 6)), transform=self.axes.transAxes, fontsize=12, color='grey')
        
        # Adjust the size of the plot area to accommodate text annotations
        plt.subplots_adjust(right=0.74, left=0.065)  # Increase the right margin

        # plot the line we think its best
        self.axes.plot(regression_x, regression_y)

        # Create a FigureCanvas widget
        self.canvas = FigureCanvas(self.figure)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        
    def drawMultiChart(self, dataDict, isMultiChart):
        # Create a Matplotlib figure and axes
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('X-axis')
        self.axes.set_ylabel('Y-axis')
        self.axes.set_title('Matplotlib Graph')

        for i in range(len(isMultiChart)):
            dataKey = isMultiChart[i]
            print(dataDict)
            listX = dataDict[dataKey]["listX"]
            slope = dataDict[dataKey]["slope"]
            intercept = dataDict[dataKey]["intercept"]

            gap = max(listX) - min(listX)
            lowX = min(listX) - gap/10
            highX = max(listX) + gap/10
            regression_x = np.linspace(0 if lowX<0 else lowX, highX, 100)
            regression_y = [ intercept + slope*number for number in regression_x ]

            # plot the line we think its best
            self.axes.plot(regression_x, regression_y, label=dataKey)
        
        self.axes.legend()
        # Create a FigureCanvas widget
        self.canvas = FigureCanvas(self.figure)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.canvas)