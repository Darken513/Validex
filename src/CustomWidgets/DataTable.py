from PyQt4 import QtGui, QtCore

class CustomLineEdit(QtGui.QLineEdit):
    lastSelectedField = None
    def __init__(self, col, row):
        self.col = col
        self.row = row
        super(CustomLineEdit, self).__init__()
        self.setStyleSheet("background-color:white;")

    def focusInEvent(self, event):
        super(CustomLineEdit, self).focusInEvent(event)
        wrapperWidget = self.parentWidget()
        wrapperWidget.setStyleSheet("background-color:rgb(220, 235, 220);")
        cellWidget = wrapperWidget.parentWidget()
        qTable = cellWidget.parentWidget()
        self.resetLastSelectedStyle(qTable)

        hLabel = qTable.cellWidget(0, self.col)
        hLabel.setStyleSheet("background-color:rgb(220, 235, 220); font-weight:bold;")
        vLabel = qTable.cellWidget(self.row, 0)
        vLabel.setStyleSheet("background-color:rgb(220, 235, 220); font-weight:bold;")
        CustomLineEdit.lastSelectedField = self

    def resetLastSelectedStyle(self, qTable):
        try:
            if( 
                CustomLineEdit.lastSelectedField != None and
                CustomLineEdit.lastSelectedField.parentWidget() != self.parentWidget() 
            ):
                CustomLineEdit.lastSelectedField.parentWidget().setStyleSheet("")
                hLabel = qTable.cellWidget(0, CustomLineEdit.lastSelectedField.col)
                hLabel.setStyleSheet("")
                vLabel = qTable.cellWidget(CustomLineEdit.lastSelectedField.row, 0)
                vLabel.setStyleSheet("")
        except:
            pass

class DataTable(QtGui.QWidget):
    def __init__(self, rows, columns):
        super(DataTable, self).__init__()
        self.rows = rows+2
        self.columns = columns+1
        self.initUI()

    def initUI(self):
        self.table = QtGui.QTableWidget(self.rows, self.columns, self)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        for col in range(0, self.columns):
            label = QtGui.QLabel('' if col==0 else 'Serie '+str(col))
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.table.setCellWidget(0, col, label)
        
        for row in range(0, self.rows):
            label = QtGui.QLabel('' if row==0 or row==1 else 'Test '+str(row-1))
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.table.setCellWidget(row, 0, label)
        
        for col in range(1, self.columns):
            wrapper = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            layout.setContentsMargins(5, 0, 5, 0)
            wrapper.setLayout(layout)
            
            labelX = QtGui.QLabel('X')
            labelX.setAlignment(QtCore.Qt.AlignCenter)

            labelY = QtGui.QLabel('Y')
            labelY.setAlignment(QtCore.Qt.AlignCenter)

            layout.addWidget(labelX)
            layout.addWidget(labelY)

            self.table.setCellWidget(1, col, wrapper)

        self.table.setStyleSheet("QTableWidget::item { margin: 0; }")

        # Set input fields in the remaining cells
        for row in range(2, self.rows):
            for col in range(1, self.columns):
                wrapper = QtGui.QWidget()
                layout = QtGui.QHBoxLayout()
                layout.setContentsMargins(5, 0, 5, 0)
                wrapper.setLayout(layout)
                
                line_edit_x = CustomLineEdit(col, row)
                float_validator = QtGui.QDoubleValidator(self)
                line_edit_x.setValidator(float_validator)
                line_edit_x.setAlignment(QtCore.Qt.AlignRight)
                line_edit_x.setPlaceholderText('0')

                line_edit_y = CustomLineEdit(col, row)
                float_validator = QtGui.QDoubleValidator(self)
                line_edit_y.setValidator(float_validator)
                line_edit_y.setAlignment(QtCore.Qt.AlignRight)
                line_edit_y.setPlaceholderText('0')

                layout.addWidget(line_edit_x)
                layout.addWidget(line_edit_y)

                self.table.setCellWidget(row, col, wrapper)
        for col in range(self.columns):
            if(col == 0):
                self.table.setColumnWidth(col, 80)
            else: 
                self.table.setColumnWidth(col, 150)
        # Set layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def fetchData(self):
        # to do : 
        # let n be the number of series
        # let m be the number of tests in each serie
        # return an array containing n lists of m lists of 2 values 
        # this allows us to save the information of what results belongs to what serie. 
        fullData = []
        for col in range(1, self.columns):
            columnData = []
            for row in range(2, self.rows):
                widget = self.table.cellWidget(row, col)
                textX = str(widget.layout().itemAt(0).widget().text())
                textY = str(widget.layout().itemAt(1).widget().text())
                columnData.append([
                    0 if textX=='' else float(textX), 
                    0 if textX=='' else float(textY)
                ])
            fullData.append(columnData)
        return fullData
    
    def clearContents(self):
        for row in range(2, self.rows):
            for col in range(1, self.columns):
                widget = self.table.cellWidget(row, col)
                widget.layout().itemAt(0).widget().setText('')
                widget.layout().itemAt(1).widget().setText('')

    def fillData(self, data):
        for colIdx in range(len(data)):
            for rowIdx in range(len(data[colIdx])):
                wrapper = self.table.cellWidget(rowIdx+2, colIdx+1)
                wrapper.layout().itemAt(0).widget().setText('' if data[colIdx][rowIdx][0]==0 else str(data[colIdx][rowIdx][0]))
                wrapper.layout().itemAt(1).widget().setText('' if data[colIdx][rowIdx][1]==0 else str(data[colIdx][rowIdx][1]))

    def keyPressEvent(self, event):
        return
        print("Tab button pressed!")