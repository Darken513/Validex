from PyQt4 import QtGui, QtCore

class InterpretationTable(QtGui.QWidget):
    def __init__(self, rowsLabels, colsLabels, data):
        super(InterpretationTable, self).__init__()
        self.data = data
        self.rowsLabels = rowsLabels
        self.colsLabels = colsLabels
        self.initUI()

    def initUI(self):
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        numberOfRows = len(self.rowsLabels) + ( 1 if len(self.colsLabels) else 0 )
        numberOfRows = len(self.colsLabels) + ( 1 if len(self.colsLabels) else 0 )
        for row in range(0, numberOfRows):
            lineLayout = QtGui.QHBoxLayout()
            lineLayout.setContentsMargins(0, 0, 0, 0)
            lineLayout.setSpacing(0)
            lineWidget = QtGui.QWidget()
            lineWidget.setLayout(lineLayout)
            if(row==0):
                for col in range(0, len(self.colsLabels)+1):
                    label = QtGui.QLabel('' if col==0 else self.colsLabels[col-1])
                    label.setProperty('class', 'tableColsHeader')
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    lineLayout.addWidget(label)
            else:
                for col in range(0, len(self.colsLabels)+1):
                    label = QtGui.QLabel(self.rowsLabels[row-1] if col==0 else str(self.data[row-1][col-1]))
                    label.setProperty('class', 'lightTableElement' if row%2 else 'DarkTableElement')
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    lineLayout.addWidget(label)
            layout.addWidget(lineWidget)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("""
            QLabel.tableElement{
                font-size: 18px;
                padding: 12px;
                max-width: 160px;
                min-width: 160px;
                font-weight: 400;
                margin:0;
                border:none;
            }
            QLabel.lightTableElement{
                font-size: 18px;
                padding: 12px;
                max-width: 240px;
                min-width: 240px;
                margin:0;
                border:none;
            }
            QLabel.DarkTableElement{
                font-size: 18px;
                padding: 12px;
                max-width: 240px;
                min-width: 240px;
                background-color: #e0e0e0;
                margin:0;
                border:none;
            }
            QLabel.tableColsHeader{
                font-size: 18px;
                padding: 12px;
                max-width: 240px;
                min-width: 240px;
                background-color: #79bbbc;
                margin:0;
                border:none;
            }
        """)