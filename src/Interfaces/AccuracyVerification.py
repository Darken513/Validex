from PyQt4 import QtGui, QtCore
import CustomWidgets.InterpretationTable as IT
from Utilities import CochrantTest, FisherTest, StudentTest
import numpy as np
import math

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
        
        self.drawGeneralMathTable()
        self.drawSlopeInterceptTable()
        self.drawFirstInterpretationTable()
        self.drawSecondInterpretationTable()
   
    def intArray_toStrArray(self, arr):
        temp = []
        for i in range(len(arr)):
            temp.append(str(arr[i]))
        return temp
    def strArray_tointArray(self, arr):
        temp = []
        for i in range(len(arr)):
            temp.append(int(arr[i]))
        return temp
    
    def drawGeneralMathTable(self):
        isStandard = self.mainScreen.data['inputState'] == '100% standard'
        slopes = self.mainScreen.data['days_B_case1' if isStandard else 'days_B_A_case2']['slopes']
        intercepts = [] if isStandard else self.mainScreen.data['days_B_A_case2']['intercepts']
        data = self.mainScreen.data['RD_full']
        n = len(data)
        m = len(data[0])
        
        self.data["qi_x"] = []
        self.data["qi_y"] = []
        self.data["qr_x"] = []
        for i in range(n):
            tempIx = []
            tempIy = []
            tempR = []
            for j in range(m):
                tempIx.append(data[i][j][0])
                tempIy.append(data[i][j][1])
                tempR.append(round(data[i][j][1] / slopes[j], 2) if isStandard else round((data[i][j][1] - intercepts[j]) / slopes[j], 2))
            self.data["qi_x"].append(tempIx)
            self.data["qi_y"].append(tempIy)
            self.data["qr_x"].append(tempR)
            
        self.data["recoveries"] = []
        for i in range(n):
            temp = []
            for j in range(m):
                temp.append(round((self.data["qr_x"][i][j] / data[i][j][0])*100, 2))
            self.data["recoveries"].append(temp)
        
        self.data["s2j"] = []
        for i in range(n):
            mean_y = sum(self.data["recoveries"][i]) / m
            variance = sum((y - mean_y)**2 for y in self.data["recoveries"][i]) / (m-1)
            self.data["s2j"].append(variance)
            
        sideLabels = []
        for i in range(n):
            temp = []
            for j in range(m):
                temp.append('{0}/{1}'.format(i+1, j+1))
            sideLabels.append(temp)
        
        lines = []
        for i in range(n):
            cols = []
            cols.append(data[i])                    
            lines.append(cols)
            
        tableData = []
        for i in range(n):
            line = []
            line.append([self.intArray_toStrArray(self.data["qi_x"][i]), 'multilines'])
            line.append([self.intArray_toStrArray(self.data["qi_y"][i]), 'multilines'])
            line.append([self.intArray_toStrArray(self.data["qr_x"][i]), 'multilines'])
            line.append([self.intArray_toStrArray(self.data["recoveries"][i]), 'multilines'])
            line.append(str(round(self.data["s2j"][i], 5)))
            tableData.append(line)
            
        widget = IT.InterpretationTable(
            sideLabels,
            [
                'Quantity <br> introduced Xij',
                'Response <br> Yij',
                'Quantity <br> recovered',
                'Recoveries',
                'S2j'
            ],
            tableData,
            [ 'mini','mini', 'mini', 'mini', 'mini', 'mini' ]
        )
        self.contentHolderLayout.addWidget(widget)

    def drawSlopeInterceptTable(self):
        isStandard = self.mainScreen.data['inputState'] == '100% standard'
        if(isStandard):
            slopes = self.mainScreen.data['days_B_case1']['slopes']
        else:
            slopes = self.mainScreen.data['days_B_A_case2']['slopes']
            intercepts = self.mainScreen.data['days_B_A_case2']['intercepts']
         
        data = self.mainScreen.data['RD_full']
        m = len(data[0])
        headers = []
        for i in range(1, m+1):
            headers.append('Day'+str(i))
        widget = IT.InterpretationTable(
            ['Slopes'] if isStandard else ['Slopes', 'Intercepts'],
            headers,
            [ self.intArray_toStrArray(slopes) ] if isStandard else [ self.intArray_toStrArray(slopes), self.intArray_toStrArray(intercepts) ],
            ['mini']*(len(headers)+1)
        )
        widget.layout.setContentsMargins(0, 20, 0, 0)
        self.contentHolderLayout.addWidget(widget)
    
    def drawFirstInterpretationTable(self):
        data = self.mainScreen.data['RD_full']
        n = len(data)
        m = len(data[0])
        CC = round(max(self.data["s2j"])/sum(self.data["s2j"]), 3)
        CT = CochrantTest.cochranCVTable(0.05, n, m-1)

        FT = FisherTest.fisherCVTable(0.05, n-1, n*m-n)
        
        Y = np.array([[0.0]*m]*n)
        for j in range(n):
            for i in range(m):
                Y[j][i] = self.data['recoveries'][j][i]
        SumT2 = FisherTest.calculate_VTotal(n, m, Y)
        SumE2 = FisherTest.calculate_VerreurExp(n, m, Y)*(n*m - n)
        varE2 = SumE2/(n*m - n)
        SumC2 = SumT2 - SumE2
        varC2 = SumC2/(n-1)
        F3 = round(varC2/varE2, 2)
        
        widget = IT.InterpretationTable(
            ["Homogenity of variances test", "Test of validity of averages"],
            ["Calculated value", "Tabulated value", "Interpretation"],
            [
                [ 
                    CC,
                    CT, 
                    "Variances are homogeneous <br> at risk alpha 0.05" if CC < CT else "Variances are not homogeneous <br> at risk alpha 0.05"
                ],
                [
                    F3, 
                    FT, 
                    "Non significant" if FT > F3 else "Significant"
                ] 
            ],
            ['large', "small", "small", "large"]
        )
        widget.layout.setContentsMargins(0, 20, 0, 0)
        self.contentHolderLayout.addWidget(widget)
    
    def drawSecondInterpretationTable(self):
        data = self.mainScreen.data['RD_full']
        n = len(data)
        m = len(data[0])
        recoveries = np.array(self.data['recoveries'])
        AVG_recov = round(sum(sum(recoveries))/(n*m), 3)
        
        std_deviation = np.std(recoveries)
        ICRange = round(StudentTest.tStudentCV(0.05, (n*m)-1)*std_deviation/math.sqrt(n*m-1), 2)
        print("L'ecart type est :", ICRange)
        print(StudentTest.tStudentCV(0.05, (n*m)-1))
        widget = IT.InterpretationTable(
            [],
            ["Confidence interval", "Average of recoveries"],
            [[str(AVG_recov)+"% with a range <br>of "+str(ICRange)+"% meaning <br>"+str(AVG_recov-ICRange)+" to "+str(AVG_recov+ICRange)+"%", str(AVG_recov)+"%"]],
            ['large', 'large']
        )
        widget.layout.setContentsMargins(0, 20, 0, 0)
        self.contentHolderLayout.addWidget(widget)