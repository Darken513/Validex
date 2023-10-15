from PyQt4 import QtGui, QtCore
import Utilities.Style as Style

# rowsLabels is an array
# rowsLabels items could be either an str:
class InterpretationTable(QtGui.QWidget):
    def __init__(self, rowsLabels, colsLabels, data, colsStyle=None):
        """
        rowsLabels: list
            items could be either an str or a list
            case list : it will be drawn as a single QLabel in one line
            case list : each element of the list will be drawn as a QLabel in a seperate line
        
        colsLabels: list
            items should be of type str only
        
        data: list of lists
                flags : 'multilines' (to draw multiple QLabels under each other)
                        'header_data' (this means that row_data itself is an array)
                        
        colsStyle : list of keywords ( should be of size cols nbr )
            keywords could be one of the following : 
                - 'mini' : it means that the entire col will be lowest widnes 
                - 'small' : it means that the entire col will be low widnes 
                - 'inherit' : it means that the entire col will be of normal widnes 
                - 'large' : it means that the entire col will be of large widnes 
        """
        super(InterpretationTable, self).__init__()
        self.data = data
        self.rowsLabels = rowsLabels
        self.colsLabels = colsLabels
        self.colsStyle = colsStyle if colsStyle else ['inherit'] * (len(self.colsLabels) + 1)
        self.initUI()

    def initUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        numberOfRows = len(self.data) + ( 1 if len(self.colsLabels) else 0 )
        for row in range(0, numberOfRows):
            lineLayout = QtGui.QHBoxLayout()
            lineLayout.setContentsMargins(0, 0, 0, 0)
            lineLayout.setSpacing(0)
            lineLayout.addStretch(1)
            lineWidget = QtGui.QWidget()
            lineWidget.setLayout(lineLayout)
            if(row==0):
                for col in range(0, len(self.colsLabels) + ( 1 if len(self.rowsLabels) else 0 )):
                    self.buildHeaderCol(self.colsLabels[col-1], col, lineLayout)
            else:
                for col in range(0, len(self.colsLabels) + ( 1 if len(self.rowsLabels) else 0 )):
                    self.buildDataCol(row, col, lineLayout)
            self.layout.addWidget(lineWidget)
            lineLayout.addStretch(1)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(Style.INTERPOLATION_TABLE_STYLES)
        
    def buildHeaderCol(self, data, col, lineLayout):
        widget = QtGui.QWidget()
        label = QtGui.QLabel('' if col==0 and len(self.rowsLabels) else data)
        widget.setProperty('class', self.getColHeaderStyle(col))
        label.setAlignment(QtCore.Qt.AlignCenter)
        widget.layout = QtGui.QVBoxLayout()
        widget.setLayout(widget.layout)
        widget.layout.setContentsMargins(0, 0, 0, 0)
        widget.layout.addWidget(label)
        lineLayout.addWidget(widget)
        
    def buildDataCol(self, row, col, lineLayout):
        widget = QtGui.QWidget()
        widget.layout = QtGui.QVBoxLayout()
        widget.layout.setContentsMargins(0, 0, 0, 0)
        widget.layout.setSpacing(0)
        widget.setLayout(widget.layout)
        widget.setProperty('class', self.getColElementStyle(col, not row%2))
        data = self.rowsLabels[row-1] if col==0 and len(self.rowsLabels) else self.data[row-1][col-1]
        if isinstance(data, str) or isinstance(data, float) or isinstance(data, int) :
            label = QtGui.QLabel(str(data))
            label.setAlignment(QtCore.Qt.AlignCenter)
            widget.layout.addWidget(label)

        if isinstance(data, list):
            self.buildDataColCaseArray(widget, col==0, data)
        
        lineLayout.addWidget(widget)
        
    def buildDataColCaseArray(self, widget, isRowHeader, data):
        if(isRowHeader):
            separator = "<br>"
            label = QtGui.QLabel(separator.join(data))
            label.setAlignment(QtCore.Qt.AlignCenter)
            widget.layout.addWidget(label)
        else:
            if(data[1] == 'multilines'):
                separator = "<br>"
                label = QtGui.QLabel(separator.join(data[0]))
                label.setAlignment(QtCore.Qt.AlignCenter)
                widget.layout.addWidget(label)
            elif(data[1] == 'minitable'):
                headerWidget = QtGui.QWidget()
                headerWidget.layout = QtGui.QHBoxLayout()
                dataWidget = QtGui.QWidget()
                dataWidget.layout = QtGui.QHBoxLayout()

                for i in range(len(data[0])):
                    headerVal = data[0][i]
                    
                    headerLabel = QtGui.QLabel(headerVal[0])
                    headerLabel.setProperty('class', 'miniTable_QLabel miniTable_QLabelHeader')
                    headerLabel.setAlignment(QtCore.Qt.AlignCenter)
                    headerWidget.layout.addWidget(headerLabel)
                    headerWidget.layout.setContentsMargins(0, 0, 0, 0)
                    headerWidget.layout.setSpacing(0)
                    
                    dataLabel = QtGui.QLabel(headerVal[1])
                    dataLabel.setProperty('class', 'miniTable_QLabel')
                    dataLabel.setAlignment(QtCore.Qt.AlignCenter)
                    dataWidget.layout.addWidget(dataLabel)
                    dataWidget.layout.setContentsMargins(0, 0, 0, 0)
                    dataWidget.layout.setSpacing(0)
                    
                headerWidget.setLayout(headerWidget.layout)
                dataWidget.setLayout(dataWidget.layout)

                widget.layout.addWidget(headerWidget)
                widget.layout.addWidget(dataWidget)
    
    def getColHeaderStyle(self, col):
        style = self.colsStyle[col] if len(self.colsStyle) else "inherit"
        if(style == 'inherit'):
            return 'tableColsHeader'  
        if(style == 'small'):
            return 'tableColsHeaderSmall'
        if(style == 'mini'):
            return 'tableColsHeaderMini'
        if(style == 'large'):
            return 'tableColsHeaderLarge'
        
    def getColElementStyle(self, col, isDark):
        style = self.colsStyle[col] if len(self.colsStyle) else "inherit"
        if(style == 'inherit'):
            return 'DarkTableElement' if isDark else 'lightTableElement'
        if(style == 'small'):
            return 'DarkTableElementSmall' if isDark else 'lightTableElementSmall'
        if(style == 'mini'):
            return 'DarkTableElementMini' if isDark else 'lightTableElementMini'
        if(style == 'large'):
            return 'DarkTableElementLarge' if isDark else 'lightTableElementLarge'