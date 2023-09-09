from PyQt4 import QtGui, QtCore
import BasicDataScreen
import AccuracyVerification
import ReconstitutedDataScreen
import ControlDataScreen
import LinearVerification
import Utilities.Style as Style

EMPTY_DATA = {
    "RSD_series_nbr": 5,
    "RSD_test_nbr": 3,
    "CSD_series_nbr": 5,
    "CSD_test_nbr": 3,
    "Refrence_idx": 3,
    "RD_full":[
        [[96.5, 76626.0], [96.8, 75154.0], [96.7, 76049.0]], 
        [[130.0, 103197.0], [129.8, 101786.0], [129.7, 101858.0]], 
        [[161.8, 128105.0], [161.5, 126865.0], [161.2, 127788.0]], 
        [[195.5, 155967.0], [195.3, 153848.0], [195.3, 153608.0]], 
        [[227.8, 181879.0], [228.6, 180355.0], [228.2, 180909.0]]
    ],
    "CD_full":[
        [[97.2, 76521.0], [97.0, 75251.0], [96.8, 75297.0]], 
        [[130.5, 102749.0], [131.2, 102210.0], [131.0, 102283.0]], 
        [[161.1, 126779.0], [163.0, 127242.0], [161.2, 126801.0]], 
        [[194.1, 153035.0], [194.1, 151598.0], [194.5, 153867.0]], 
        [[226.4, 178584.0], [225.6, 176002.0], [225.9, 178332.0]]
    ],
}

class Screen(QtGui.QMainWindow):
    def __init__(self):
        super(Screen, self).__init__()
        self.data = {
            "RSD_series_nbr": 5,
            "RSD_test_nbr": 3,
            "CSD_series_nbr": 5,
            "CSD_test_nbr": 3,
            "Refrence_idx": 3,
            "RD_full":[
                [[96.5, 76626.0], [96.8, 75154.0], [96.7, 76049.0]], 
                [[130.0, 103197.0], [129.8, 101786.0], [129.7, 101858.0]], 
                [[161.8, 128105.0], [161.5, 126865.0], [161.2, 127788.0]], 
                [[195.5, 155967.0], [195.3, 153848.0], [195.3, 153608.0]], 
                [[227.8, 181879.0], [228.6, 180355.0], [228.2, 180909.0]]
            ],
            "CD_full":[
                [[97.2, 76521.0], [97.0, 75251.0], [96.8, 75297.0]], 
                [[130.5, 102749.0], [131.2, 102210.0], [131.0, 102283.0]], 
                [[161.1, 126779.0], [163.0, 127242.0], [161.2, 126801.0]], 
                [[194.1, 153035.0], [194.1, 151598.0], [194.5, 153867.0]], 
                [[226.4, 178584.0], [225.6, 176002.0], [225.9, 178332.0]]
            ],
        }
        self.toolBarBtns = []
        self.setWindowTitle("VALIDEX")
        self.initToolBar()
        self.initDividedWindows()
        self.initBasicDataScreen()

    def initToolBar(self):
        toolbar = QtGui.QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        button1 = QtGui.QPushButton('Basic data', self)
        button1.clicked.connect(self.initBasicDataScreen)
        button2 = QtGui.QPushButton('Reconstituted data', self)
        button2.clicked.connect(self.initReconstitutedDataScreen)
        button3 = QtGui.QPushButton('Control data', self)
        button3.clicked.connect(self.initControldDataScreen)
        button4 = QtGui.QPushButton('Linearity', self)
        button4.clicked.connect(self.initLinearVerificationScreen)
        button5 = QtGui.QPushButton('Accuracy', self)
        button5.clicked.connect(self.initAccuracyVerificationScreen)
        button6 = QtGui.QPushButton('Reliability', self)

        toolbar.addWidget(button1)
        toolbar.addWidget(button2)
        toolbar.addWidget(button3)
        toolbar.addWidget(button4)
        toolbar.addWidget(button5)
        toolbar.addWidget(button6)

        self.toolBarBtns.extend([button1, button2, button3, button4, button5, button6])
        for btn in self.toolBarBtns:
            btn.setStyleSheet(Style.TOOLBAR_BTN_DISABLED)
            if(btn != self.toolBarBtns[0]):
                btn.setEnabled(False)
            else:
                btn.setCursor(QtCore.Qt.PointingHandCursor)

        # todo :
        # add the navigation system
        # add the fact that some buttons are unclickable at first

    def initDividedWindows(self):
        self.centralWidget = QtGui.QWidget()
        self.layout = QtGui.QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)

        self.leftWindow = QtGui.QScrollArea()
        self.leftWindow.setMinimumSize(200,300)

        self.layout.addWidget(self.leftWindow)

        self.rightWindow = QtGui.QScrollArea()
        self.rightWindow.setMinimumSize(200,300)
        self.layout.addWidget(self.rightWindow)
    
    def initBasicDataScreen(self):
        self.leftWindow = QtGui.QScrollArea()
        self.leftWindow.setMinimumSize(200,300)
        widget = self.layout.itemAt(0).widget()
        if(widget):
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.layout.insertWidget(0, self.leftWindow)
        self.leftWindow.setWidget(BasicDataScreen.Screen(self))
        self.initEmptyDataMsg()

    def initReconstitutedDataScreen(self):
        ReconstitutedDataScreen.Screen(self)

    def initControldDataScreen(self):
        ControlDataScreen.Screen(self)

    def initLinearVerificationScreen(self):
        LinearVerification.Screen(self)
        
    def initAccuracyVerificationScreen(self):
        AccuracyVerification.Screen(self)

    def initEmptyDataMsg(self):
        if(
            self.data["RSD_series_nbr"] == None or
            self.data["RSD_test_nbr"] == None or
            self.data["CSD_series_nbr"] == None or
            self.data["CSD_test_nbr"] == None or
            self.data["RD_full"] == None or
            self.data["CD_full"] == None
        ):
            label = QtGui.QLabel("No data to use")
            label.setStyleSheet("padding:100%; font-size:24px; color:rgb(180,180,180);")
            
            item = self.layout.takeAt(1)
            widget = item.widget()
            self.layout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
            #draw new widget on the right side
            self.rightWindow = QtGui.QScrollArea()
            self.rightWindow.setMinimumSize(200,300)
            self.layout.addWidget(self.rightWindow)
            self.rightWindow.setWidget(label)
            for btn in self.toolBarBtns[3:]:
                btn.setStyleSheet(Style.TOOLBAR_BTN_DISABLED)
                btn.setEnabled(False)

    def onBasicDataScreenEvent(self, event):
        if(event['msg'] == 'submit' and event['data']):
            self.data["RSD_series_nbr"] = event["data"]["RSD_series_nbr"]
            self.data["RSD_test_nbr"] = event["data"]["RSD_test_nbr"]
            self.data["CSD_series_nbr"] = event["data"]["CSD_series_nbr"]
            self.data["CSD_test_nbr"] = event["data"]["CSD_test_nbr"]
            self.data["Refrence_idx"] = event["data"]["Refrence_idx"]
            for btn in self.toolBarBtns[1:3]:
                btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.setEnabled(True)
            self.initReconstitutedDataScreen()

        elif(event['msg'] == 'reset'):
            #EMPTY_DATA
            self.data = { 
                "RSD_series_nbr": None,
                "RSD_test_nbr": None,
                "CSD_series_nbr": None,
                "CSD_test_nbr": None,
                "Refrence_idx": None,
                "RD_full":None,
                "CD_full":None,
            }
            for btn in self.toolBarBtns[1:]:
                btn.setStyleSheet(Style.TOOLBAR_BTN_DISABLED)
                btn.setEnabled(False)
            self.initEmptyDataMsg()

        elif(event['msg'] == 'unchanged'):
            for btn in self.toolBarBtns[1:3]:
                btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.setEnabled(True)
            self.initReconstitutedDataScreen()

    def onReconstitutedDataScreenEvent(self, event):
        if(event['msg'] == 'submit' and event['data']):
            self.data["RD_full"] = event["data"]["RD_full"]
            self.initControldDataScreen()

        elif(event['msg'] == 'reset'):
            self.data["RD_full"] = None
            self.initEmptyDataMsg()

        elif(event['msg'] == 'unchanged'):
            self.initControldDataScreen()

    def onControlDataScreenEvent(self, event):
        if(event['msg'] == 'submit' and event['data']):
            self.data["CD_full"] = event["data"]["CD_full"]
            self.initLinearVerificationScreen()

        elif(event['msg'] == 'reset'):
            self.data["CD_full"] = None
            self.initEmptyDataMsg()

        elif(event['msg'] == 'unchanged'):
            self.initLinearVerificationScreen()

    def updateToolBarBtnsStyle(self, idxOn, activateTillIdx=0):
        for i in range(len(self.toolBarBtns)):
            btn = self.toolBarBtns[i]
            if(i<=activateTillIdx):
                btn.setEnabled(True)
            if(btn == self.toolBarBtns[idxOn]):
                btn.setEnabled(True)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.setStyleSheet(Style.TOOLBAR_BTN_ON)
            else:
                if(btn.isEnabled()):
                    btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)
                    btn.setCursor(QtCore.Qt.PointingHandCursor)
                else:
                    btn.setStyleSheet(Style.TOOLBAR_BTN_DISABLED)