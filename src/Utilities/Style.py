TOOLBAR_BTN_ON = """
    QPushButton
    {
        border-top-left-radius:10px;
        border-top-right-radius:10px; 
        border:1px solid rgb(80,120,80); 
        padding:10px 15px; 
        margin:1px; 
        background-color: rgb(180,230,180)
    }       
"""

TOOLBAR_BTN_OFF = """
    QPushButton
    {
        border-top-left-radius:10px;
        border-top-right-radius:10px; 
        border:1px solid rgb(170,170,170); 
        padding:10px 15px; 
        margin:1px; 
        background-color: rgb(215,235,215)
    } 
    QPushButton:hover
    {
        background-color: rgb(225,240,225)
    } 
"""

TOOLBAR_BTN_DISABLED = """
    QPushButton
    {
        border-top-left-radius:10px;
        border-top-right-radius:10px; 
        border:1px solid rgb(205,205,205); 
        padding:10px 15px; 
        margin:1px; 
        background-color: rgb(220,220,220);
        color: rgb(170,170,170);
    } 
"""

SUBMIT_BUTTON = """
    QPushButton
    {
        border:none;
        border-radius:10px; 
        background-color: rgb(180,235,180);
        padding: 10px;
        font-weight: 600;
    }
    QPushButton:disabled
    {
        background-color: rgb(210,215,210);
    }
    QPushButton:hover
    {
        background-color: rgb(190,245,190);
    }
"""
RESET_BUTTON = """
    QPushButton
    {
        border:none;
        border-radius:10px; 
        background-color: rgb(245,160,160);
        padding: 10px;
        font-weight: 600;
    }
    QPushButton:hover
    {
        background-color: rgb(255,175,175);
    }
"""

INTERPOLATION_TABLE_STYLES = """
    QLabel{
        border:none;
        margin:0;
        padding: 10px;
        max-width: 140px;
        min-width: 140px;
    }
    QWidget.tableColsHeader QLabel,
    QWidget.lightTableElement QLabel,
    QWidget.DarkTableElement QLabel{
        border:none;
        margin:0;
        padding: 10px;
        max-width: 210px;
        min-width: 210px;
    }
    QWidget.tableColsHeaderSmall QLabel,
    QWidget.lightTableElementSmall QLabel,
    QWidget.DarkTableElementSmall QLabel{
        border:none;
        margin:0;
        padding: 10px;
        max-width: 180px;
        min-width: 180px;
    }
    QLabel.miniTable_QLabelHeader,
    QLabel.miniTable_QLabelHeader,
    QLabel.miniTable_QLabelHeader{
        background-color: rgb(180,230,180);
    } 
    QWidget.tableColsHeader QLabel.miniTable_QLabel,
    QWidget.lightTableElement QLabel.miniTable_QLabel,
    QWidget.DarkTableElement QLabel.miniTable_QLabel{
        border:none;
        margin:0;
        padding: 10px 5px;
        max-width: 105px;
        min-width: 105px;
    }
    QWidget.tableColsHeaderSmall QLabel.miniTable_QLabel,
    QWidget.lightTableElementSmall QLabel.miniTable_QLabel,
    QWidget.DarkTableElementSmall QLabel.miniTable_QLabel{
        border:none;
        margin:0;
        padding: 10px 5px;
        max-width: 90px;
        min-width: 90px;
    }
    QWidget.tableColsHeaderLarge QLabel.miniTable_QLabel,
    QWidget.lightTableElementLarge QLabel.miniTable_QLabel,
    QWidget.DarkTableElementLarge QLabel.miniTable_QLabel{
        border:none;
        margin:0;
        padding: 10px 5px;
        max-width: 120px;
        min-width: 120px;
    }
    QWidget.tableColsHeaderLarge QLabel,
    QWidget.lightTableElementLarge QLabel,
    QWidget.DarkTableElementLarge QLabel{
        border:none;
        margin:0;
        padding: 10px;
        max-width: 260px;
        min-width: 260px;
    }
    QWidget.tableColsHeader{
        font-size: 18px;
        max-width: 230px;
        min-width: 230px;
        background-color: rgb(180,230,180);
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.tableColsHeaderSmall{
        font-size: 18px;
        max-width: 200px;
        min-width: 200px;
        background-color: rgb(180,230,180);
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.tableColsHeaderLarge{
        font-size: 18px;
        max-width: 280px;
        min-width: 280px;
        background-color: rgb(180,230,180);
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.lightTableElement{
        font-size: 18px;
        max-width: 230px;
        min-width: 230px;
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.lightTableElementSmall{
        font-size: 18px;
        max-width: 200px;
        min-width: 200px;
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.lightTableElementLarge{
        font-size: 18px;
        max-width: 280px;
        min-width: 280px;
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.DarkTableElement{
        font-size: 18px;
        max-width: 230px;
        min-width: 230px;
        background-color: #e0e0e0;
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.DarkTableElementSmall{
        font-size: 18px;
        max-width: 200px;
        min-width: 200px;
        background-color: #e0e0e0;
        margin:0;
        padding:0;
        border:none;
    }
    QWidget.DarkTableElementLarge{
        font-size: 18px;
        max-width: 280px;
        min-width: 280px;
        background-color: #e0e0e0;
        margin:0;
        padding:0;
        border:none;
    }
"""