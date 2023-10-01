from PyQt4 import QtGui, QtCore
import ReconstitutedDataScreen as RDS

class Screen(RDS.Screen):
    def updateMainScreenUI(self):
        self.mainScreen.updateToolBarBtnsStyle(2)

    def initParams(self):
        self.testDatakey = 'CSD_test_nbr'
        self.seriesDatakey = 'CSD_series_nbr'
        self.dataFull = 'CD_full'

    def onSubmit(self):
        data = self.tableWrapper.fetchData()
        event = {}
        event = {
            "msg":'submit', 
            "data":{self.dataFull:data}
        }
        self.callbackParent(event)

    def callbackParent(self, event):
        self.mainScreen.onControlDataScreenEvent(event) 