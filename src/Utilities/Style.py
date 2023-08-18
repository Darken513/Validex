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
    QLabel.tableElement{
        font-size: 18px;
        padding: 12px;
        max-width: 160px;
        min-width: 160px;
        font-weight: 400;
        margin:0;
        border:none;
    }
    QLabel.tableColsHeader{
        font-size: 18px;
        padding: 12px;
        max-width: 220px;
        min-width: 220px;
        background-color: rgb(180,230,180);
        margin:0;
        border:none;
    }
    QLabel.tableColsHeaderSmall{
        font-size: 18px;
        padding: 12px;
        max-width: 170px;
        min-width: 170px;
        background-color: rgb(180,230,180);
        margin:0;
        border:none;
    }
    QLabel.tableColsHeaderLarge{
        font-size: 18px;
        padding: 12px;
        max-width: 270px;
        min-width: 270px;
        background-color: rgb(180,230,180);
        margin:0;
        border:none;
    }
    QLabel.lightTableElement{
        font-size: 18px;
        padding: 12px;
        max-width: 220px;
        min-width: 220px;
        margin:0;
        border:none;
    }
    QLabel.lightTableElementSmall{
        font-size: 18px;
        padding: 12px;
        max-width: 170px;
        min-width: 170px;
        margin:0;
        border:none;
    }
    QLabel.lightTableElementLarge{
        font-size: 18px;
        padding: 12px;
        max-width: 270px;
        min-width: 270px;
        margin:0;
        border:none;
    }
    QLabel.DarkTableElement{
        font-size: 18px;
        padding: 12px;
        max-width: 220px;
        min-width: 220px;
        background-color: #e0e0e0;
        margin:0;
        border:none;
    }
    QLabel.DarkTableElementSmall{
        font-size: 18px;
        padding: 12px;
        max-width: 170px;
        min-width: 170px;
        background-color: #e0e0e0;
        margin:0;
        border:none;
    }
    QLabel.DarkTableElementLarge{
        font-size: 18px;
        padding: 12px;
        max-width: 270px;
        min-width: 270px;
        background-color: #e0e0e0;
        margin:0;
        border:none;
    }
"""