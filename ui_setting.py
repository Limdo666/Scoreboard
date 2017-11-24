# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        SettingDialog.setObjectName("SettingDialog")
        SettingDialog.resize(391, 239)
        SettingDialog.setModal(True)
        self.label = QtWidgets.QLabel(SettingDialog)
        self.label.setGeometry(QtCore.QRect(50, 20, 101, 17))
        self.label.setObjectName("label")
        self.btn_ok = QtWidgets.QPushButton(SettingDialog)
        self.btn_ok.setGeometry(QtCore.QRect(80, 190, 89, 25))
        self.btn_ok.setObjectName("btn_ok")
        self.edit_mem_size = QtWidgets.QLineEdit(SettingDialog)
        self.edit_mem_size.setGeometry(QtCore.QRect(160, 20, 113, 25))
        self.edit_mem_size.setObjectName("edit_mem_size")
        self.btn_cancel = QtWidgets.QPushButton(SettingDialog)
        self.btn_cancel.setGeometry(QtCore.QRect(240, 190, 89, 25))
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayoutWidget = QtWidgets.QWidget(SettingDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 60, 289, 112))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.edit_add_count = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_add_count.setObjectName("edit_add_count")
        self.gridLayout.addWidget(self.edit_add_count, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.edit_mul_count = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_mul_count.setObjectName("edit_mul_count")
        self.gridLayout.addWidget(self.edit_mul_count, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.edit_div_count = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_div_count.setObjectName("edit_div_count")
        self.gridLayout.addWidget(self.edit_div_count, 4, 1, 1, 1)
        self.edit_add_delay = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_add_delay.setObjectName("edit_add_delay")
        self.gridLayout.addWidget(self.edit_add_delay, 2, 2, 1, 1)
        self.edit_mul_delay = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_mul_delay.setObjectName("edit_mul_delay")
        self.gridLayout.addWidget(self.edit_mul_delay, 3, 2, 1, 1)
        self.edit_div_delay = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.edit_div_delay.setObjectName("edit_div_delay")
        self.gridLayout.addWidget(self.edit_div_delay, 4, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)

        self.retranslateUi(SettingDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingDialog)

    def retranslateUi(self, SettingDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingDialog.setWindowTitle(_translate("SettingDialog", "Setting"))
        self.label.setText(_translate("SettingDialog", "Memory Size: "))
        self.btn_ok.setText(_translate("SettingDialog", "OK"))
        self.edit_mem_size.setText(_translate("SettingDialog", "100"))
        self.btn_cancel.setText(_translate("SettingDialog", "Cancel"))
        self.edit_add_count.setText(_translate("SettingDialog", "1"))
        self.label_2.setText(_translate("SettingDialog", "Division Units:"))
        self.label_5.setText(_translate("SettingDialog", "Multiplication Units: "))
        self.edit_mul_count.setText(_translate("SettingDialog", "2"))
        self.label_4.setText(_translate("SettingDialog", "Addition Units:"))
        self.edit_div_count.setText(_translate("SettingDialog", "1"))
        self.edit_add_delay.setText(_translate("SettingDialog", "2"))
        self.edit_mul_delay.setText(_translate("SettingDialog", "10"))
        self.edit_div_delay.setText(_translate("SettingDialog", "40"))
        self.label_6.setText(_translate("SettingDialog", "Count"))
        self.label_7.setText(_translate("SettingDialog", "Delay"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SettingDialog = QtWidgets.QDialog()
    ui = Ui_SettingDialog()
    ui.setupUi(SettingDialog)
    SettingDialog.show()
    sys.exit(app.exec_())

