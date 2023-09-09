from PyQt4 import QtGui, QtCore
import CustomWidgets.InterpretationTable as IT
import Utilities.FisherTest as FisherTest
import Utilities.AccuarcyMath as AccuarcyMath

class Screen(QtGui.QWidget):
    def __init__(self, mainScreen):
        super(Screen, self).__init__()
        self.data = {}
        self.state = 0 #0 for D1, 1 for D2, 2 for Statistics
        self.mainScreen = mainScreen 
        self.initUI()
        self.updateMainScreenUI()

    def updateMainScreenUI(self):
        self.mainScreen.updateToolBarBtnsStyle(4)
        #delete right side
        item = self.mainScreen.layout.takeAt(1)
        widget = item.widget()
        self.mainScreen.layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()
        #draw new widget on the right side
        self.mainScreen.layout.addWidget(self)

    def initUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 0, 0, 0)
        
        self.scrollAreaWidget = QtGui.QScrollArea()
        self.contentHolderWidget = QtGui.QWidget()
        self.contentHolderLayout = QtGui.QVBoxLayout()
        self.contentHolderWidget.setLayout(self.contentHolderLayout)
        self.layout.addWidget(self.scrollAreaWidget)

        self.redrawInner()
        self.scrollAreaWidget.setWidget(self.contentHolderWidget)

    def redrawInner(self):
        titleText = ""
        if(self.state == 0):
            titleText = "Reconstituted data graph :"
        else:
            titleText = "Control data graph :"
        
        # Delete all widgets under the layout
        while self.contentHolderLayout.count():
            item = self.contentHolderLayout.takeAt(0)
            widget = item.widget()
            self.contentHolderLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        
        #Redraw all
        title = QtGui.QLabel(titleText)
        title.setProperty('class', 'title')
        self.contentHolderLayout.addWidget(title)

        self.drawInterpretationTable()
    
    def drawInterpretationTable(self):
        days_B_case1 = AccuarcyMath.calculateSlopePerSeries100(self.mainScreen.data["CD_full"], self.mainScreen.data["Refrence_idx"]-1)
        days_B_A_case2 = AccuarcyMath.calculateSlopePerSeries_CD(self.mainScreen.data["CD_full"])
        print(days_B_case1)