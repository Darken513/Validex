from PyQt4 import QtGui, QtCore
import Utilities.Style as Style
import CustomWidgets.LinearGraph as LG
import CustomWidgets.InterpretationTable as IT
from scipy import stats

class Screen(QtGui.QWidget):
    def __init__(self, mainScreen):
        super(Screen, self).__init__()
        self.data = {}
        self.currentScreen = 0 #0 for D1, 1 for D2, 2 for Statistics
        self.mainScreen = mainScreen 
        self.toolBarBtns = []
        self.initToolBar()
        self.initUI()
        self.updateMainScreenUI()

    def updateMainScreenUI(self):
        self.mainScreen.updateToolBarBtnsStyle(3)
        self.mainScreen.rightWindow.setWidget(self)

    def initToolBar(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 0, 0, 0)

        toolbar = QtGui.QToolBar()
        toolbar.setMovable(False)
        self.layout.addWidget(toolbar)

        button1 = QtGui.QPushButton('D1 Linearity verification', self)
        button1.clicked.connect(self.initD1Screen)
        button2 = QtGui.QPushButton('D2 Linearity verification', self)
        button2.clicked.connect(self.initD2Screen)
        button3 = QtGui.QPushButton('Statistics study', self)

        toolbar.addWidget(button1)
        toolbar.addWidget(button2)
        toolbar.addWidget(button3)

        self.toolBarBtns.extend([button1, button2, button3])
        for btn in self.toolBarBtns:
            btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            if(btn == self.toolBarBtns[0]):
                btn.setStyleSheet(Style.TOOLBAR_BTN_ON)
        
        # todo :
        # add the navigation system
        # add the fact that some buttons are unclickable at first

    def initUI(self):
        self.calculateD1Details()
        self.redrawInner()

    def initD1Screen(self):
        self.calculateD1Details()
        self.redrawInner()

    def initD2Screen(self):
        self.calculateD2Details()
        self.redrawInner()

    def redrawInner(self):
        titleText = ""
        if(self.currentScreen == 0):
            titleText = "D1 graph :"
        elif(self.currentScreen == 1):
            titleText = "D2 graph :"
        else:
            return #treat it in different method

        # Delete all widgets under the layout
        while self.layout.count()!=1:
            item = self.layout.takeAt(1)
            widget = item.widget()
            self.layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        
        #Redraw all
        title = QtGui.QLabel(titleText)
        title.setProperty('class', 'title')
        self.layout.addWidget(title)

        widget = LG.MatplotlibWidget(self.data)
        self.layout.addWidget(widget)

        equation = str(round(self.data["intercept"], 3))+" + "+str(round(self.data["slope"], 3))+" . X"
        
        self.addLabelValueGroup("The equation :", equation)
        self.addLabelValueGroup("Slope :", str(round(self.data["slope"], 6)))
        self.addLabelValueGroup("Intercept :", str(round(self.data["intercept"], 6)))
        self.addLabelValueGroup("Correlation coefficient :", str(round(self.data["r_value"], 6)))
       
        widget = IT.InterpretationTable(
            [
                'Homogenity of variances test',
                'Slope existence test',
                'validity of adjustments'
            ],
            [
                'Calculated value',
                'Tabulated value',
                'Interpretation'
            ],
            [
                [1,2,3],
                [4,5,6],
                [6,7,8]
            ]
        )
        self.layout.addWidget(widget)
        
        self.setStyleSheet("""
            QLabel{
                font-size: 18px;
                padding: 12px;
                max-width: 210px;
                min-width: 210px;
                border:1px solid rgb(80,80,80);
            }
            QLabel.title{
                border:none;
                color: rgb(60,60,60);
                font-size:25px;
                min-width: 210px;
                max-width: none;
                margin-bottom:0;
                padding-bottom:0;
            }
            QLabel.labelHolder{
                max-width: 210px;
                min-width: 210px;
                color: rgb(210,120,120);
            }
        """)

    def addLabelValueGroup(self, label, value):
        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        labelHolder = QtGui.QLabel(label)
        labelHolder.setProperty('class', 'labelHolder')
        valueHolder = QtGui.QLabel(value)
        layout.addWidget(labelHolder)
        layout.addWidget(valueHolder)
        layout.addStretch()
        self.layout.addWidget(widget)
        
    def calculateD1Details(self):
        self.updateToolBarBtnsStyle(0)
                
        self.data["listX"] = []
        self.data["listY"] = []
        for subarray in self.mainScreen.data["RD_full"]:
            for i in range(len(subarray)):
                self.data["listX"].append(subarray[i][0])
                self.data["listY"].append(subarray[i][1])

        slope, intercept, r_value, p_value, std_err = stats.linregress(self.data["listX"], self.data["listY"])

        self.data["slope"] = slope
        self.data["intercept"] = intercept
        self.data["r_value"] = r_value

        if(std_err):
            print(std_err, "an error has occured")       

    def calculateD2Details(self):
        self.updateToolBarBtnsStyle(1)
        
        self.data["listX"] = []
        self.data["listY"] = []
        for subarray in self.mainScreen.data["CD_full"]:
            for i in range(len(subarray)):
                self.data["listX"].append(subarray[i][0])
                self.data["listY"].append(subarray[i][1])

        slope, intercept, r_value, p_value, std_err = stats.linregress(self.data["listX"], self.data["listY"])

        self.data["slope"] = slope
        self.data["intercept"] = intercept
        self.data["r_value"] = r_value

        if(std_err):
            print(std_err, "an error has occured")

    def updateToolBarBtnsStyle(self, idxOn):
        for btn in self.toolBarBtns:
            if(btn == self.toolBarBtns[idxOn]):
                btn.setStyleSheet(Style.TOOLBAR_BTN_ON)
            else:
                btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)