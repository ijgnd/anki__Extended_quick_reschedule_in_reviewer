# -*- coding: utf-8 -*-
# License: AGPLv3

from aqt import mw
from anki import version

if version.startswith("2.1."):
    from PyQt5.QtCore import Qt, QTimer, QSize
    from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QShortcut, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QSizePolicy
    from PyQt5.QtGui import QKeySequence
else:
    from PyQt4.QtCore import Qt, QTimer, QSize
    from PyQt4.QtGui import QHBoxLayout, QPushButton, QShortcut, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QLineEdit, QSizePolicy
    from PyQt4.QtGui import QKeySequence
from aqt.qt import *


from .forms import reschedule



class MultiPrompt(QDialog):
    """ """

    def __init__(self, co):
        self.co = co
        parent = mw.app.activeWindow()
        QDialog.__init__(self, parent)
        self.setWindowModality(Qt.WindowModal)
        self.qrs = reschedule.Ui_Dialog() 
        self.qrs.setupUi(self)
        self.setupHotkeys()
        
        self.qrs.lineEdit.textChanged.connect(self.checkText) #https://stackoverflow.com/q/22520747
        self.qrs.lineEdit.installEventFilter(self)  #https://stackoverflow.com/questions/47960368

        self.qrs.tb_up.setArrowType(Qt.UpArrow)
        self.qrs.tb_up.clicked.connect(lambda _: self.on_arrows(1))

        self.qrs.tb_down.setArrowType(Qt.DownArrow)
        self.qrs.tb_down.clicked.connect(lambda _: self.on_arrows(-1))

        self.qrs.pbc_clear.clicked.connect(lambda: self.qrs.lineEdit.setText(str(0)))
        self.qrs.pbc_enter.clicked.connect(self.accept_read_lineedit)
            
        if not self.co['add_num_area_to_dialog']:  
            #hide calculator like input
            #for some reason it doesn't suffice to hide self.qrs.vL_calc.setParent(None)   
            #if I just run this I will see one remaing button on the upper left of the window
            self.qrs.pbc0.setParent(None) 
            self.qrs.pbc1.setParent(None) 
            self.qrs.pbc2.setParent(None) 
            self.qrs.pbc3.setParent(None) 
            self.qrs.pbc4.setParent(None) 
            self.qrs.pbc5.setParent(None) 
            self.qrs.pbc6.setParent(None) 
            self.qrs.pbc7.setParent(None) 
            self.qrs.pbc8.setParent(None) 
            self.qrs.pbc9.setParent(None) 
            self.qrs.pbc_enter.setParent(None)
            self.qrs.pbc_clear.setParent(None)
            self.qrs.vL_calc.setParent(None)

        self.qrs.pbc0.clicked.connect(lambda: self.add_to_display(0))
        self.qrs.pbc1.clicked.connect(lambda: self.add_to_display(1))
        self.qrs.pbc2.clicked.connect(lambda: self.add_to_display(2))
        self.qrs.pbc3.clicked.connect(lambda: self.add_to_display(3))
        self.qrs.pbc4.clicked.connect(lambda: self.add_to_display(4))
        self.qrs.pbc5.clicked.connect(lambda: self.add_to_display(5))
        self.qrs.pbc6.clicked.connect(lambda: self.add_to_display(6))
        self.qrs.pbc7.clicked.connect(lambda: self.add_to_display(7))
        self.qrs.pbc8.clicked.connect(lambda: self.add_to_display(8))
        self.qrs.pbc9.clicked.connect(lambda: self.add_to_display(9))
        
        self.qrs.pb_u_clear.clicked.connect(lambda: self.qrs.lineEdit.setText(str(0)))
        self.qrs.pb_u_accept.clicked.connect(self.accept_read_lineedit)
        self.qrs.pb_u_accept.setDefault(True)
        self.qrs.pb_u_cancel.clicked.connect(self.close)
        
        self.qrs.lineEdit.setFocus()


        if self.co['add_quick_buttons_to_dialog']:
            for v in self.co['quick_buttons']:
                k = QPushButton()
                k.setMinimumSize(QSize(0, 53))   #53 is the height of the buttons in the top row
                k.setText(v['label'])
                k.clicked.connect(lambda _,v=v['ivl']: self.set_and_accept(v))
                self.qrs.vL_custom.addWidget(k)
            qf = QPushButton()
            qf.setMinimumSize(QSize(0, 53))   #53 is the height of the buttons in the top row
            qf.setText('forget')
            qf.clicked.connect(lambda: self.set_and_accept(0))
            self.qrs.vL_custom.addWidget(qf)

    def checkText(self,arg):
        try:
           int(arg)
        except:
            if not (arg == "+" or arg == "-"):
                self.qrs.lineEdit.setText(self.qrs.lineEdit.text()[:-1])
        else:
            pass
    
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyPress and source is self.qrs.lineEdit):
            #if (event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_E):
            if self.co['secondary_accept_1']:  
                if (event.key() == eval('Qt.Key_' + str(self.co['secondary_accept_1']).title()) and not self.qrs.lineEdit.text() == ""):         
                    self.accept_read_lineedit()
                    return True
            if self.co['secondary_accept_2']:         
                if (event.key() == eval('Qt.Key_' + str(self.co['secondary_accept_2']).title()) and not self.qrs.lineEdit.text() == ""):
                    self.accept_read_lineedit()
                    return True
            if (event.key() == eval('Qt.Key_' + str(self.co['one_more_day']).title())):
                self.change_value_of_display(1)
                return True
            if (event.key() == eval('Qt.Key_' + str(self.co['one_less_day']).title())):
                self.change_value_of_display(-1)
                return True
            if (event.key() == eval('Qt.Key_' + str(self.co['relearn_key']).title())):  
                self.set_and_accept(0)
                return True
            elif self.co['add_quick_buttons_to_dialog']:
                for v in self.co['quick_buttons']:
                    if event.key() == eval('Qt.Key_' + str(v['key'].title())):                   
                        self.set_and_accept(v['ivl'])
                        return True
        return False

    def accept_read_lineedit(self):
        if len(self.qrs.lineEdit.text()) == 0:
            return
        days = int(self.qrs.lineEdit.text())
        self.set_and_accept(days)

    def set_and_accept(self,days):
        print('in selfaccept ' + str(days))
        self.days = days
        self.accept()

    def change_value_of_display(self,num):
        if self.qrs.lineEdit.text() == "":
            val = 0
        else:
            val = int(self.qrs.lineEdit.text())
        newval = val+num
        self.qrs.lineEdit.setText(str(newval))

    def add_to_display(self,num):
        if (self.qrs.lineEdit.text() == "" and num == 0):
            pass
        else:
            newstring = self.qrs.lineEdit.text() + str(num)
            self.qrs.lineEdit.setText(newstring)

    def on_arrows(self, num):
        if self.qrs.lineEdit.text() == "":
            self.qrs.lineEdit.setText(str(0))
        newstring = int(self.qrs.lineEdit.text()) + num
        self.qrs.lineEdit.setText(str(newstring))

    def setupHotkeys(self):
        if self.co['add_quick_buttons_to_dialog']:    
            s = QShortcut(QKeySequence(str(self.co['relearn_key'])),            self, activated=lambda: self.set_and_accept(0,0))
            s = QShortcut(QKeySequence(str(self.co['focus_lineedit'])),         self, activated=lambda: self.qrs.lineEdit.setFocus())
            s = QShortcut(QKeySequence(str(self.co['one_more_day'])),           self, activated=lambda: self.change_value_of_display(1))
            s = QShortcut(QKeySequence(str(self.co['one_less_day'])),           self, activated=lambda: self.change_value_of_display(-1))

            for v in self.co['quick_buttons']:
                s = QShortcut(QKeySequence(str(v['key'])),     self, activated=lambda: self.set_and_accept(v['ivl']))

            if self.co['secondary_accept_1']:    
                s = QShortcut(QKeySequence(str(self.co['secondary_accept_1'])), self, activated=lambda: self.accept_read_lineedit())
            if self.co['secondary_accept_2']:
                s = QShortcut(QKeySequence(str(self.co['secondary_accept_2'])), self, activated=lambda: self.accept_read_lineedit())
