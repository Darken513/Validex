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

        for row in range(0, len(self.rowsLabels)+1):
            lineLayout = QtGui.QHBoxLayout()
            lineLayout.setContentsMargins(0, 0, 0, 0)
            lineLayout.setSpacing(0)
            lineWidget = QtGui.QWidget()
            lineWidget.setLayout(lineLayout)
            if(row==0):
                for col in range(0, len(self.colsLabels)+1):
                    label = QtGui.QLabel('' if col==0 else self.colsLabels[col-1])
                    label.setProperty('class', 'tableRowHeader' if col==0 else 'tableElement')
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    lineLayout.addWidget(label)
            else:
                for col in range(0, len(self.colsLabels)+1):
                    label = QtGui.QLabel(self.rowsLabels[row-1] if col==0 else str(self.data[row-1][col-1]))
                    label.setProperty('class', 'tableRowHeader' if col==0 else 'tableElement')
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
                border:1px solid rgb(80,80,80);
            }
            QLabel.tableRowHeader{
                font-size: 18px;
                padding: 12px;
                max-width: 240px;
                min-width: 240px;
                margin:0;
                border:1px solid rgb(80,80,80);
            }
        """)