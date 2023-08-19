from PyQt4 import QtGui, QtCore
import Utilities.Style as Style
import CustomWidgets.LinearGraph as LG
import CustomWidgets.InterpretationTable as IT
from scipy import stats
import Interfaces.StatisticsStudy as StatisticsStudy
import Utilities.CochrantTest as CochrantTest
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
        button3.clicked.connect(self.initStatisticsScreen)

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
        # for initial calculation, should calculate both, then use them for reference
        self.calculateD2Details()
        self.calculateD1Details()
        self.redrawInner()
        self.scrollAreaWidget.setWidget(self.contentHolderWidget)

    def initD1Screen(self):
        self.updateToolBarBtnsStyle(0)
        self.currentScreen = 0
        self.redrawInner()

    def initD2Screen(self):
        self.updateToolBarBtnsStyle(1)
        self.currentScreen = 1
        self.redrawInner()

    def initStatisticsScreen(self):
        StatisticsStudy.Screen(self)
        
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

        data = self.data['Reconstituted data graph (D1)'] if self.currentScreen==0 else self.data['Control data graph (D2)']
        
        widget = LG.MatplotlibWidget(data, False)
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
        data = self.data['Reconstituted data graph (D1)'] if self.currentScreen==0 else self.data['Control data graph (D2)']
        n = self.mainScreen.data["RSD_series_nbr" if self.currentScreen == 0 else "CSD_series_nbr"]
        m = self.mainScreen.data["RSD_test_nbr" if self.currentScreen == 0 else "CSD_test_nbr"]
        b = data["slope"]
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
        data = {}      
        data["listX"] = []
        data["listY"] = []
        for subarray in self.mainScreen.data["RD_full"]:
            for i in range(len(subarray)):
                data["listX"].append(subarray[i][0])
                data["listY"].append(subarray[i][1])

        slope, intercept, r_value, p_value, std_err = stats.linregress(data["listX"], data["listY"])

        data["slope"] = slope
        data["intercept"] = intercept
        data["r_value"] = r_value

        self.data['Reconstituted data graph (D1)'] = data
        
        if(std_err):
            print(std_err, "an error has occured")       

        self.currentScreen = 0

    def calculateD2Details(self):
        data = {}
        
        data["listX"] = []
        data["listY"] = []
        for subarray in self.mainScreen.data["CD_full"]:
            for i in range(len(subarray)):
                data["listX"].append(subarray[i][0])
                data["listY"].append(subarray[i][1])

        slope, intercept, r_value, p_value, std_err = stats.linregress(data["listX"], data["listY"])

        data["slope"] = slope
        data["intercept"] = intercept
        data["r_value"] = r_value
        
        self.data['Control data graph (D2)'] = data

        if(std_err):
            print(std_err, "an error has occured")
        

    def updateToolBarBtnsStyle(self, idxOn):
        for btn in self.toolBarBtns:
            if(btn == self.toolBarBtns[idxOn]):
                btn.setStyleSheet(Style.TOOLBAR_BTN_ON)
            else:
                btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)