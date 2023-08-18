from PyQt4 import QtGui, QtCore
import Utilities.Style as Style
import CustomWidgets.LinearGraph as LG
import CustomWidgets.InterpretationTable as IT
from scipy import stats
import Utilities.CochrantTest as CochrantTest
import Utilities.StudentTest as StudentTest
import Utilities.FisherTest as FisherTest

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
        #delete right side
        item = self.mainScreen.layout.takeAt(1)
        widget = item.widget()
        self.mainScreen.layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()
        #draw new widget on the right side
        self.mainScreen.layout.addWidget(self)

    def initToolBar(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 0, 0, 0)

        toolbar = QtGui.QToolBar()
        toolbar.setMovable(False)
        self.layout.addWidget(toolbar)

        button1 = QtGui.QPushButton('Reconstituted data Linearity verification', self)
        button1.clicked.connect(self.initD1Screen)
        button2 = QtGui.QPushButton('Control data Linearity verification', self)
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
        self.scrollAreaWidget = QtGui.QScrollArea()
        #self.scrollAreaWidget.setStyleSheet("background-color: white;")
        self.contentHolderWidget = QtGui.QWidget()
        self.contentHolderLayout = QtGui.QVBoxLayout()
        self.contentHolderWidget.setLayout(self.contentHolderLayout)
        self.layout.addWidget(self.scrollAreaWidget)
        self.calculateD1Details()
        self.redrawInner()
        self.scrollAreaWidget.setWidget(self.contentHolderWidget)

    def initD1Screen(self):
        self.calculateD1Details()
        self.redrawInner()

    def initD2Screen(self):
        self.calculateD2Details()
        self.redrawInner()

    def redrawInner(self):
        titleText = ""
        if(self.currentScreen == 0):
            titleText = "Reconstituted data graph :"
        elif(self.currentScreen == 1):
            titleText = "Control data graph :"
        else:
            return #treat it in different method
        
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

        widget = LG.MatplotlibWidget(self.data)
        self.contentHolderLayout.addWidget(widget)
       
        self.drawInterpretationTable()
        
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
                font-weight: 500;
                min-width: 360px;
                max-width: none;
                margin-bottom:0;
                padding-bottom:0;
            }
            QLabel.labelHolder{
                max-width: 210px;
                min-width: 210px;
                background-color: #79bbbc;
                color: black;
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
        self.contentHolderLayout.addWidget(widget)
    
    def drawInterpretationTable(self):
        print("currentScreen", self.currentScreen)
        n = self.mainScreen.data["RSD_series_nbr" if self.currentScreen == 0 else "CSD_series_nbr"]
        m = self.mainScreen.data["RSD_test_nbr" if self.currentScreen == 0 else "CSD_test_nbr"]
        b = self.data["slope"]
        xy = self.mainScreen.data["RD_full" if self.currentScreen == 0 else "CD_full"]
        
        CT = CochrantTest.couchranValue(n, m, b, xy)
        C_CV = CochrantTest.cochranCVTable(0.05, n, m-1)
        
        FHS = FisherTest.calculateFisherHS(n, m, b, xy)
        FHS_CV = FisherTest.fisherCVTable(0.05, 1, n*m-2)
        
        FNS = FisherTest.calculateFisherNS(n, m, b, xy)
        FNS_CV = FisherTest.fisherCVTable(0.05, n-2, n*m-n)
        
        widget = IT.InterpretationTable(
            [
                'Homogenity of variances test',
                'Slope existence test',
                'Validity of adjustments'
            ],
            [
                'Calculated value',
                'Tabulated value',
                'Interpretation'
            ],
            [
                [ CT , 'C(0.05, {}, {})='.format(str(n), str(m-1)) + str(C_CV) , ('Non Significant' if CT < C_CV else 'Significant') ],
                [ FHS, 'F(0.05, 1, {})='.format(str(n*m-2)) + str(FHS_CV), ('Non Significant' if FHS < FHS_CV else 'Highly Significant') ],
                [ FNS, 'F(0.05, {}, {})='.format(str(n-2), str(n*m-n)) + str(FNS_CV), ('Non Significant' if FNS < FNS_CV else 'Significant') ]
            ],
            [ 'large', 'small', 'inherit', 'inherit' ]
        )
        self.contentHolderLayout.addWidget(widget)
        
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

        self.currentScreen = 0

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
        
        self.currentScreen = 1

    def updateToolBarBtnsStyle(self, idxOn):
        for btn in self.toolBarBtns:
            if(btn == self.toolBarBtns[idxOn]):
                btn.setStyleSheet(Style.TOOLBAR_BTN_ON)
            else:
                btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)