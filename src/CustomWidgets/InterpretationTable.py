from PyQt4 import QtGui, QtCore
import Utilities.Style as Style

class InterpretationTable(QtGui.QWidget):
    def __init__(self, rowsLabels, colsLabels, data, colsStyle=None):
        super(InterpretationTable, self).__init__()
        self.data = data
        self.rowsLabels = rowsLabels
        self.colsLabels = colsLabels
        self.colsStyle = colsStyle if colsStyle else ['inherit']* (len(self.colsLabels) + 1)
        self.initUI()

    def initUI(self):
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        numberOfRows = len(self.rowsLabels) + ( 1 if len(self.colsLabels) else 0 )
        for row in range(0, numberOfRows):
            lineLayout = QtGui.QHBoxLayout()
            lineLayout.setContentsMargins(0, 0, 0, 0)
            lineLayout.setSpacing(0)
            lineWidget = QtGui.QWidget()
            lineWidget.setLayout(lineLayout)
            if(row==0):
                for col in range(0, len(self.colsLabels)+1):
                    label = QtGui.QLabel('' if col==0 else self.colsLabels[col-1])
                    label.setProperty('class', self.getColHeaderStyle(col))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    lineLayout.addWidget(label)
            else:
                for col in range(0, len(self.colsLabels)+1):
                    label = QtGui.QLabel(self.rowsLabels[row-1] if col==0 else str(self.data[row-1][col-1]))
                    label.setProperty('class', self.getColElementStyle(col, not row%2))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    lineLayout.addWidget(label)
            layout.addWidget(lineWidget)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.INTERPOLATION_TABLE_STYLES)
        
    def getColHeaderStyle(self, col):
        style = self.colsStyle[col] if len(self.colsStyle) else "inherit"
        if(style == 'inherit'):
            return 'tableColsHeader'  
        if(style == 'small'):
            return 'tableColsHeaderSmall'
        if(style == 'large'):
            return 'tableColsHeaderLarge'
        
    def getColElementStyle(self, col, isDark):
        style = self.colsStyle[col] if len(self.colsStyle) else "inherit"
        if(style == 'inherit'):
            return 'DarkTableElement' if isDark else 'lightTableElement'
        if(style == 'small'):
            return 'DarkTableElementSmall' if isDark else 'lightTableElementSmall'
        if(style == 'large'):
            return 'DarkTableElementLarge' if isDark else 'lightTableElementLarge'