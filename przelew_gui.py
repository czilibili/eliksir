# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'przelew_gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CzasPrzelewu(object):
    def setupUi(self, CzasPrzelewu):
        CzasPrzelewu.setObjectName(_fromUtf8("CzasPrzelewu"))
        CzasPrzelewu.resize(276, 334)
        self.gridLayout = QtGui.QGridLayout(CzasPrzelewu)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lab_bank_nad = QtGui.QLabel(CzasPrzelewu)
        self.lab_bank_nad.setObjectName(_fromUtf8("lab_bank_nad"))
        self.gridLayout.addWidget(self.lab_bank_nad, 0, 0, 1, 1)
        self.bank_nadawca = QtGui.QComboBox(CzasPrzelewu)
        self.bank_nadawca.setObjectName(_fromUtf8("bank_nadawca"))
        self.gridLayout.addWidget(self.bank_nadawca, 0, 1, 1, 1)
        self.lab_bank_odb = QtGui.QLabel(CzasPrzelewu)
        self.lab_bank_odb.setObjectName(_fromUtf8("lab_bank_odb"))
        self.gridLayout.addWidget(self.lab_bank_odb, 1, 0, 1, 1)
        self.bank_odbiorca = QtGui.QComboBox(CzasPrzelewu)
        self.bank_odbiorca.setObjectName(_fromUtf8("bank_odbiorca"))
        self.gridLayout.addWidget(self.bank_odbiorca, 1, 1, 1, 1)
        self.lab_czas_zlec = QtGui.QLabel(CzasPrzelewu)
        self.lab_czas_zlec.setObjectName(_fromUtf8("lab_czas_zlec"))
        self.gridLayout.addWidget(self.lab_czas_zlec, 2, 0, 1, 1)
        self.timeEdit = QtGui.QTimeEdit(CzasPrzelewu)
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.gridLayout.addWidget(self.timeEdit, 2, 1, 1, 1)
        self.butt_ok = QtGui.QPushButton(CzasPrzelewu)
        self.butt_ok.setObjectName(_fromUtf8("butt_ok"))
        self.gridLayout.addWidget(self.butt_ok, 3, 1, 1, 1)
        self.butt_close = QtGui.QPushButton(CzasPrzelewu)
        self.butt_close.setObjectName(_fromUtf8("butt_close"))
        self.gridLayout.addWidget(self.butt_close, 4, 1, 1, 1)

        self.retranslateUi(CzasPrzelewu)
        QtCore.QMetaObject.connectSlotsByName(CzasPrzelewu)

    def retranslateUi(self, CzasPrzelewu):
        CzasPrzelewu.setWindowTitle(_translate("CzasPrzelewu", "O której przelew", None))
        self.lab_bank_nad.setText(_translate("CzasPrzelewu", "Bank nadawca", None))
        self.lab_bank_odb.setText(_translate("CzasPrzelewu", "Bank odbiorca", None))
        self.lab_czas_zlec.setText(_translate("CzasPrzelewu", "Godzina zlecenia", None))
        self.butt_ok.setText(_translate("CzasPrzelewu", "OK", None))
        self.butt_close.setText(_translate("CzasPrzelewu", "Zamknij", None))

