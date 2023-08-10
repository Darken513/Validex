from PyQt4 import QtGui, QtCore
import BasicDataScreen
import ReconstitutedDataScreen
import ControlDataScreen
import LinearVerification
import Utilities.Style as Style

EMPTY_DATA = {
    "RSD_series_nbr": None,
    "RSD_test_nbr": None,
    "CSD_series_nbr": None,
    "CSD_test_nbr": None,
    "RD_full":None,
    "CD_full":None,
}

class Screen(QtGui.QMainWindow):
    def __init__(self):
        super(Screen, self).__init__()
        self.data = {
            "RSD_series_nbr": None,
            "RSD_test_nbr": None,
            "CSD_series_nbr": None,
            "CSD_test_nbr": None,
            "RD_full":None,
            "CD_full":None,
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
            self.rightWindow.setWidget(label)

    def onBasicDataScreenEvent(self, event):
        if(event['msg'] == 'submit' and event['data']):
            self.data["RSD_series_nbr"] = event["data"]["RSD_series_nbr"]
            self.data["RSD_test_nbr"] = event["data"]["RSD_test_nbr"]
            self.data["CSD_series_nbr"] = event["data"]["CSD_series_nbr"]
            self.data["CSD_test_nbr"] = event["data"]["CSD_test_nbr"]
            for btn in self.toolBarBtns[1:3]:
                btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.setEnabled(True)
            self.initReconstitutedDataScreen()

        elif(event['msg'] == 'reset'):
            self.data = EMPTY_DATA
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
            self.initControldDataScreen()

    def updateToolBarBtnsStyle(self, idxOn):
        for btn in self.toolBarBtns:
            if(btn == self.toolBarBtns[idxOn]):
                btn.setEnabled(True)
                btn.setCursor(QtCore.Qt.PointingHandCursor)
                btn.setStyleSheet(Style.TOOLBAR_BTN_ON)
            else:
                if(btn.isEnabled()):
                    btn.setStyleSheet(Style.TOOLBAR_BTN_OFF)
                else:
                    btn.setStyleSheet(Style.TOOLBAR_BTN_DISABLED)