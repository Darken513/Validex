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
        self.drawInterpretationTableAndMsg()
    
    def drawInterpretationTableAndMsg(self):
        data1 = self.callerScreen.data['Reconstituted data graph (D1)'] 
        data2 = self.callerScreen.data['Control data graph (D2)']
        
        n1 = self.callerScreen.mainScreen.data["RSD_series_nbr"]
        m1 = self.callerScreen.mainScreen.data["RSD_test_nbr"]
        
        n2 = self.callerScreen.mainScreen.data["CSD_series_nbr"]
        m2 = self.callerScreen.mainScreen.data["CSD_test_nbr"]
        
        a1 = data1["intercept"]
        a2 = data2["intercept"]
        
        b1 = data1["slope"]
        b2 = data2["slope"]
        
        r1 = data1["r_value"]
        r2 = data2["r_value"]
        
        xy1 = self.callerScreen.mainScreen.data["RD_full"]
        xy2 = self.callerScreen.mainScreen.data["CD_full"]
        
        ICT_8 = StudentTest.calculate_TestT_ord(a1, a2, r1, r2, xy1, xy2)
        ICT_98_CV = StudentTest.tStudentCV(0.05, (n1*m1 - 2)*2)
        
        error1 = (ICT_8 > ICT_98_CV)
        CTSF_9 = "..." if error1 else StudentTest.calculate_TestT_pente(b1, b2, r1, r2, xy1, xy2)
        
        error2 = error1 or (CTSF_9 > ICT_98_CV)
        ICT0_1 = "..." if error2 else StudentTest.calculate_TestT_ord0(a1, r1, xy1)
        ICT0_2 = "..." if error2 else StudentTest.calculate_TestT_ord0(a2, r2, xy2)
        ICT0_CV = "..." if error2 else StudentTest.tStudentCV(0.05, n1*m1 - 2)
        
        widget = IT.InterpretationTable(
            [
                'Intercept comparison test',
                ['Comparison test of', 'slopes of fitting lines'],
                ['Intercept comparison', 'test with 0']
            ],
            [
                'Calculated value',
                'Tabulated value',
                'Interpretation'
            ],
            [
                [ 
                    str(ICT_8),
                    'C(0.05, {})='.format(str((n1*m1 -2)*2)) + str(ICT_98_CV),
                    ('Non Significant' if ICT_8 < ICT_98_CV else 'Significant')
                ],
                [ 
                    str(CTSF_9),
                    "..." if error1 else 'C(0.05, {})='.format(str((n1*m1 -2)*2)) + str(ICT_98_CV),
                    "..." if error1 else ('Non Significant' if CTSF_9 < ICT_98_CV else 'Significant')
                ],
                [ 
                    [[['D1', "..." if error2 else str(ICT0_1)], ['D2', "..." if error2 else str(ICT0_2)]], 'minitable'], 
                    "..." if error2 else 'C(0.05, {})='.format(str(n1*m1 -2)) + str(ICT0_CV), 
                    [[
                        ['D1', "..." if error2 else ('Non Significant' if ICT0_1 < ICT0_CV else 'Significant')], 
                        ['D2', "..." if error2 else ('Non Significant' if ICT0_2 < ICT0_CV else 'Significant')]
                    ], 'minitable']
                ]
            ],
            [ 'inherit', 'small', 'inherit', 'large' ]
        )
        self.callerScreen.contentHolderLayout.addWidget(widget)
        
        finalMessage = ""
        color = ""
        if(ICT_8 < ICT_98_CV and CTSF_9 < ICT_98_CV and ICT0_1 < ICT0_CV and ICT0_2 < ICT0_CV):
            finalMessage = "Reference system : 100% standard"
            color = " rgb(75,230,75)"
        elif(ICT_8 < ICT_98_CV and CTSF_9 < ICT_98_CV and not (ICT0_1 < ICT0_CV and ICT0_2 < ICT0_CV)):
            finalMessage = "Reference system : Calibration range"
            color = " rgb(75,255,75)"
        elif(ICT_8 > ICT_98_CV):
            finalMessage = "Matrix effect, review procedure"
            color = "red"
        elif(ICT_8 < ICT_98_CV and CTSF_9 > ICT_98_CV):
            finalMessage = "Systematic error, possible correction"
            color = "red"
        else:
            finalMessage = "Systematic error, review the provided data"
            color = "red"
                        
        label = QtGui.QLabel(finalMessage)
        label.setStyleSheet("""
            color: {0};
            border: 2px solid {0};
            font-size: 25px;
            min-width: 550px;
            padding: 10px 12px;
            border-radius: 6px;
            margin-top: 15px;
        """.format(color))
        label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.callerScreen.contentHolderLayout.addWidget(label)
        self.callerScreen.contentHolderLayout.setAlignment(label, QtCore.Qt.AlignCenter) 
        
    def generateInterpretationData():
        pass