# -*- coding: utf-8 -*-
# __author__ = 'lidong'

"""
Description:
"""

from PyQt5.QtWidgets import QDialog, QMessageBox
from ui_setting import Ui_SettingDialog

class SettingForm(QDialog):
    def __init__(self, father):
        super(SettingForm, self).__init__(father)
        self.father = father
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)
        self.ui.btn_ok.clicked.connect(self.ok)
        self.ui.btn_cancel.clicked.connect(self.close)

    def ok(self):
        setting_info = {}
        try:
            setting_info['mem_size'] = int(self.ui.edit_mem_size.text())
            setting_info['add_count'] = int(self.ui.edit_add_count.text())
            setting_info['add_delay'] = int(self.ui.edit_add_delay.text())
            setting_info['mul_count'] = int(self.ui.edit_mul_count.text())
            setting_info['mul_delay'] = int(self.ui.edit_mul_delay.text())
            setting_info['div_count'] = int(self.ui.edit_div_count.text())
            setting_info['div_delay'] = int(self.ui.edit_div_delay.text())
            self.father.setting_info = setting_info
            self.close()
        except:
            QMessageBox.information(self, 'Error', 'Contents should be integer.')
