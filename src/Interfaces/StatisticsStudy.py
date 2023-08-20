from PyQt4 import QtGui, QtCore
import Utilities.Style as Style
import CustomWidgets.LinearGraph as LG
import CustomWidgets.InterpretationTable as IT

import Utilities.CochrantTest as CochrantTest
import Utilities.StudentTest as StudentTest
import Utilities.FisherTest as FisherTest
class Screen(QtGui.QWidget):
    def __init__(self, callerScreen):
        super(Screen, self).__init__()
        self.data = {}
        self.callerScreen = callerScreen 
        self.initUI()
        self.updateCallerScreenUI()

    def updateCallerScreenUI(self):
        #update caller toolbar ( LinearVerification )
        self.callerScreen.updateToolBarBtnsStyle(2)
        #update mainscreen toolaber
        self.callerScreen.mainScreen.updateToolBarBtnsStyle(3)

    def initUI(self):
        # Delete all widgets under the layout
        while self.callerScreen.contentHolderLayout.count():
            item = self.callerScreen.contentHolderLayout.takeAt(0)
            widget = item.widget()
            self.callerScreen.contentHolderLayout.removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
        
        widget = LG.MatplotlibWidget(self.callerScreen.data, ['Reconstituted data graph (D1)', 'Control data graph (D2)'])
        self.callerScreen.contentHolderLayout.addWidget(widget)
        self.drawInterpretationTable()
    
    def drawInterpretationTable(self):
        data = self.callerScreen.data['Reconstituted data graph (D1)'] if self.callerScreen.currentScreen==0 else self.callerScreen.data['Control data graph (D2)']
        n = self.callerScreen.mainScreen.data["RSD_series_nbr" if self.callerScreen.currentScreen == 0 else "CSD_series_nbr"]
        m = self.callerScreen.mainScreen.data["RSD_test_nbr" if self.callerScreen.currentScreen == 0 else "CSD_test_nbr"]
        b = data["slope"]
        xy = self.callerScreen.mainScreen.data["RD_full" if self.callerScreen.currentScreen == 0 else "CD_full"]
        
        CT = CochrantTest.couchranValue(n, m, b, xy)
        C_CV = CochrantTest.cochranCVTable(0.05, n, m-1)
        
        FHS = FisherTest.calculateFisherHS(n, m, b, xy)
        FHS_CV = FisherTest.fisherCVTable(0.05, 1, n*m-2)
        
        FNS = FisherTest.calculateFisherNS(n, m, b, xy)
        FNS_CV = FisherTest.fisherCVTable(0.05, n-2, n*m-n)
        
        widget = IT.InterpretationTable(
            [
                'Intercept comparison test',
                ['Comparison test of', 'slopes of fitting lines'],
                'Intercept comparison test with 0'
            ],
            [
                'Calculated value',
                'Tabulated value',
                'Interpretation'
            ],
            [
                [ [[['header1', 'value1'], ['header2', 'value2']], 'minitable'], 'C(0.05, {}, {})='.format(str(n), str(m-1)) + str(C_CV) , ('Non Significant' if CT < C_CV else 'Significant') ],
                [ [['header1', 'value1', 'header2', 'value2'], 'multilines'], 'F(0.05, 1, {})='.format(str(n*m-2)) + str(FHS_CV), ('Non Significant' if FHS < FHS_CV else 'Highly Significant') ],
                [ FNS, 'F(0.05, {}, {})='.format(str(n-2), str(n*m-n)) + str(FNS_CV), [[['header1', 'value1'], ['header2', 'value2']], 'minitable']]
            ],
            [ 'large', 'small', 'inherit', 'inherit' ]
        )
        self.callerScreen.contentHolderLayout.addWidget(widget)