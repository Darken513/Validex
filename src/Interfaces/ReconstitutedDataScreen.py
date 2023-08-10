from PyQt4 import QtGui, QtCore
from CustomWidgets.DataTable import DataTable
import Utilities.Style as Style
import Utilities.UtilFunc as UF

class Screen(QtGui.QWidget):
    def __init__(self, mainScreen):
        super(Screen, self).__init__()
        self.data = {}
        self.mainScreen = mainScreen 
        self.initParams()
        self.updateMainScreenUI()
        self.initUI()
        self.initData()

    def initParams(self):
        self.testDatakey = 'RSD_test_nbr'
        self.seriesDatakey = 'RSD_series_nbr'
        self.dataFull = 'RD_full'

    def updateMainScreenUI(self):
        self.mainScreen.updateToolBarBtnsStyle(1)

    def initUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        widget = self.mainScreen.layout.itemAt(0).widget()
        if(widget):
            self.mainScreen.layout.removeWidget(widget)
            widget.deleteLater()
        
        self.tableWrapper = DataTable(
            self.mainScreen.data[self.testDatakey],
            self.mainScreen.data[self.seriesDatakey]
        )
        self.layout.addWidget(self.tableWrapper)
        self.addSubmittionBtns()
        self.mainScreen.layout.insertWidget(0, self)
        
    def initData(self):
        if(self.mainScreen.data[self.dataFull]):
            self.tableWrapper.fillData(self.mainScreen.data[self.dataFull])

    def addSubmittionBtns(self):
        wrapper = QtGui.QWidget()
        wrapper.layout = QtGui.QHBoxLayout()
        wrapper.layout.setContentsMargins(15, 2, 15, 0)
        wrapper.setLayout(wrapper.layout)

        self.submitBtn = QtGui.QPushButton('Submit')
        self.submitBtn.setStyleSheet(Style.SUBMIT_BUTTON)
        self.submitBtn.setCursor(QtCore.Qt.PointingHandCursor)
        
        self.resetBtn = QtGui.QPushButton('Reset')
        self.resetBtn.setStyleSheet(Style.RESET_BUTTON)
        self.resetBtn.setCursor(QtCore.Qt.PointingHandCursor)

        self.submitBtn.clicked.connect(self.onSubmit)
        self.resetBtn.clicked.connect(self.onReset)

        wrapper.layout.addWidget(self.submitBtn)
        wrapper.layout.addWidget(self.resetBtn)
        self.layout.addWidget(wrapper)

    def onReset(self):
        self.tableWrapper.clearContents()
        event = {"msg":"reset"}
        self.callbackParent(event)

    def onSubmit(self):
        data = self.tableWrapper.fetchData()
        event = {}
        if(UF.compareEmbeddedArrays(data, self.mainScreen.data[self.dataFull])):
            event = {'msg':"unchanged"}
        else:
            event = {
                "msg":'submit', 
                "data":{self.dataFull:data}
            }
        self.callbackParent(event)

    def callbackParent(self, event):
        self.mainScreen.onReconstitutedDataScreenEvent(event) 