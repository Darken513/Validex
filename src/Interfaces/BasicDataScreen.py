from PyQt4 import QtGui, QtCore
import Utilities.Style as Style

class Screen(QtGui.QWidget):
    def __init__(self, mainScreen):
        super(Screen, self).__init__()
        self.data = {}
        self.mainScreen = mainScreen 
        self.updateMainScreenUI()
        self.initUI()
        self.initData()

    def updateMainScreenUI(self):
        self.mainScreen.leftWindow.setMaximumWidth(400)
        self.mainScreen.updateToolBarBtnsStyle(0)

    def initUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.initRSDWrapper()
        self.initCSDWrapper()
        self.addSubmittionBtns()

    def initData(self):
        if( 
            not (
                self.mainScreen.data["RSD_series_nbr"] or 
                self.mainScreen.data["RSD_test_nbr"] or 
                self.mainScreen.data["CSD_series_nbr"] or 
                self.mainScreen.data["CSD_test_nbr"] 
            )
        ): 
            return
            
        self.data["RSD_series_nbr"] = self.mainScreen.data["RSD_series_nbr"]
        self.data["RSD_test_nbr"] = self.mainScreen.data["RSD_test_nbr"]
        self.data["CSD_series_nbr"] = self.mainScreen.data["CSD_series_nbr"]
        self.data["CSD_test_nbr"] = self.mainScreen.data["CSD_test_nbr"]

        self.inputNDS_RSD.setText(str(self.data["RSD_series_nbr"]) if self.data["RSD_series_nbr"] else "")
        self.inputMT_RSD.setText(str(self.data["RSD_test_nbr"]) if self.data["RSD_test_nbr"] else "")
        self.inputNDS_CSD.setText(str(self.data["CSD_series_nbr"]) if self.data["CSD_series_nbr"] else "")
        self.inputMT_CSD.setText(str(self.data["CSD_test_nbr"]) if self.data["CSD_test_nbr"] else "")

        self.inputNDS_RSD.setReadOnly(True)
        self.inputMT_RSD.setReadOnly(True)
        self.inputNDS_CSD.setReadOnly(True)
        self.inputMT_CSD.setReadOnly(True)

    def addLabelInputGroup(self, parentLayout, labelText, inputName):
        wrapper = QtGui.QWidget()
        wrapper.layout = QtGui.QHBoxLayout()
        wrapper.layout.setContentsMargins(15, 2, 15, 0)
        wrapper.setLayout(wrapper.layout)

        label = QtGui.QLabel(labelText)
        label.setStyleSheet("min-width:200px;")
        inputField = QtGui.QLineEdit()
        inputField.setPlaceholderText('x >= 2')
        validator = QtGui.QIntValidator(self)
        inputField.setValidator(validator)
        inputField.setAlignment(QtCore.Qt.AlignRight)
        inputField.textChanged.connect(self.onTextEdit)

        setattr(self, inputName, inputField)
        wrapper.layout.addWidget(label)
        wrapper.layout.addWidget(getattr(self, inputName))

        parentLayout.addWidget(wrapper)

    def addHorizentalSeparator(self, layout):
        separator = QtGui.QFrame()
        separator.setFrameShape(QtGui.QFrame.HLine)
        separator.setFrameShadow(QtGui.QFrame.Sunken)
        layout.addWidget(separator)

    def initRSDWrapper(self):
        header = QtGui.QLabel("Reconstituted sample data")
        header.setStyleSheet("text-decoration: underline; color:rgb(120,120,120);")
        self.layout.addWidget(header)
        self.addLabelInputGroup(self.layout, 'Number of dosing series', 'inputNDS_RSD')
        self.addLabelInputGroup(self.layout, 'Maximum number of tests', 'inputMT_RSD')
        self.addHorizentalSeparator(self.layout)

    def initCSDWrapper(self):
        header = QtGui.QLabel("Control sample data")
        header.setStyleSheet("text-decoration: underline; color:rgb(120,120,120);")
        self.layout.addWidget(header)
        self.addLabelInputGroup(self.layout, 'Number of dosing series', 'inputNDS_CSD')
        self.addLabelInputGroup(self.layout, 'Maximum number of tests', 'inputMT_CSD')
        self.addHorizentalSeparator(self.layout)

    def addSubmittionBtns(self):
        wrapper = QtGui.QWidget()
        wrapper.layout = QtGui.QHBoxLayout()
        wrapper.layout.setContentsMargins(15, 2, 15, 0)
        wrapper.setLayout(wrapper.layout)

        self.submitBtn = QtGui.QPushButton('Submit')
        self.submitBtn.setEnabled(False)

        self.resetBtn = QtGui.QPushButton('Reset')
        self.resetBtn.setStyleSheet(Style.RESET_BUTTON)
        self.resetBtn.setCursor(QtCore.Qt.PointingHandCursor)

        self.submitBtn.clicked.connect(self.onSubmit)
        self.submitBtn.setStyleSheet(Style.SUBMIT_BUTTON)

        self.resetBtn.clicked.connect(self.onReset)
        
        wrapper.layout.addWidget(self.submitBtn)
        wrapper.layout.addWidget(self.resetBtn)
        self.layout.addWidget(wrapper)

    def onTextEdit(self):
        RSD_series_nbr = int(self.inputNDS_RSD.text() if len(self.inputNDS_RSD.text())!=0 else '0')
        RSD_test_nbr = int(self.inputMT_RSD.text() if len(self.inputMT_RSD.text())!=0 else '0')
        CSD_series_nbr = int(self.inputNDS_CSD.text() if len(self.inputNDS_CSD.text())!=0 else '0')
        CSD_test_nbr = int(self.inputMT_CSD.text() if len(self.inputMT_CSD.text())!=0 else '0')
        enabled = (RSD_series_nbr != 0 and
            RSD_test_nbr != 0 and
            CSD_series_nbr !=0 and 
            CSD_test_nbr !=0 )
        self.submitBtn.setEnabled(enabled)
        if(enabled):
            self.submitBtn.setCursor(QtCore.Qt.PointingHandCursor)


    def onSubmit(self):
        # todo : m should never be less than 2 !!!!!!!!!!!!!! cause we use often in math equations m-1
        # todo : n should never be less than 3 !!!!!!!!!!!!!! cause we use often in math equations n-2
        self.data["RSD_series_nbr"] = int(self.inputNDS_RSD.text() if len(self.inputNDS_RSD.text())!=0 else '0')
        self.data["RSD_test_nbr"] = int(self.inputMT_RSD.text() if len(self.inputMT_RSD.text())!=0 else '0')
        self.data["CSD_series_nbr"] = int(self.inputNDS_CSD.text() if len(self.inputNDS_CSD.text())!=0 else '0')
        self.data["CSD_test_nbr"] = int(self.inputMT_CSD.text() if len(self.inputMT_CSD.text())!=0 else '0')

        # todo : add an error msg in case one of the tables contains 1 cell only, a line graph takes at least 2 points to draw
        if(self.inputNDS_CSD.isReadOnly()):
            self.mainScreen.onBasicDataScreenEvent({"msg":"unchanged"})
            return
        self.inputNDS_CSD.setReadOnly(True)
        self.inputMT_CSD.setReadOnly(True)
        self.inputNDS_RSD.setReadOnly(True)
        self.inputMT_RSD.setReadOnly(True)

        self.mainScreen.onBasicDataScreenEvent({"msg":"submit", "data":self.data})

    def onReset(self):
        self.inputNDS_CSD.setReadOnly(False)
        self.inputMT_CSD.setReadOnly(False)
        self.inputNDS_RSD.setReadOnly(False)
        self.inputMT_RSD.setReadOnly(False)

        self.inputNDS_CSD.setText("")
        self.inputMT_CSD.setText("")
        self.inputNDS_RSD.setText("")
        self.inputMT_RSD.setText("")

        self.data["RSD_series_nbr"] = None
        self.data["RSD_test_nbr"] = None
        self.data["CSD_series_nbr"] = None
        self.data["CSD_test_nbr"] = None
       
        self.mainScreen.onBasicDataScreenEvent({"msg":"reset"})

