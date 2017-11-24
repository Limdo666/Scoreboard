# -*- coding: utf-8 -*-
# __author__ = 'lidong'

"""
Description:
"""
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QFileDialog
from ui_mainwindow import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QColor
from settingwidget import SettingForm

from simulator import Simulator


class Mainwindow(QMainWindow):
    """
    主窗口
    """
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_run.clicked.connect(self.start)
        self.ui.btn_stop.clicked.connect(self.stop)
        self.ui.btn_pause.clicked.connect(self.pause)
        self.ui.btn_loadfile.clicked.connect(self.loadFile)
        self.ui.btn_setting.clicked.connect(self.openSettingForm)
        self.code = ''
        self.is_start = False
        self.is_pause = False

        self.setting_info = {'mem_size':100,
                             'add_count':1,
                             'add_delay':2,
                             'div_count':1,
                             'div_delay':40,
                             'mul_count':2,
                             'mul_delay':10}

    def initUI(self):
        """
        设置tabel widget 行标
        :return:
        """
        self.ui.table_registers.setColumnCount(len(self.simulator.registers))
        self.ui.table_registers.setRowCount(1)
        self.ui.table_fregisters.setColumnCount(len(self.simulator.fregisters))
        self.ui.table_fregisters.setRowCount(1)

        self.ui.table_registers.setHorizontalHeaderLabels([r.name for r in self.simulator.registers])
        self.ui.table_fregisters.setHorizontalHeaderLabels([r.name for r in self.simulator.fregisters])

        self.ui.table_instructions.setRowCount(len(self.simulator.instructions))
        self.ui.table_funcuints.setRowCount(len(self.simulator.get_all_units()))

        for i in range(len(self.simulator.instructions)):
            inst = self.simulator.instructions[i]
            self.ui.table_instructions.setItem(i, 0, QTableWidgetItem(inst.operation))
            self.ui.table_instructions.setItem(i, 1, QTableWidgetItem(inst.dest))
            self.ui.table_instructions.setItem(i, 2, QTableWidgetItem(inst.source1))
            self.ui.table_instructions.setItem(i, 3, QTableWidgetItem(inst.source2))


    def openSettingForm(self):
        self.setting = SettingForm(self)
        result = self.setting.exec()
        self.ui.run_info.append(str(result))

    @pyqtSlot()
    def start(self):
        try:
            self.stop = int(self.ui.lineedit_cycle.text())
        except Exception:
            self.stop = 0
        if not self.code:
            return

        self.is_start = True
        self.clear()
        self.simulator = Simulator(self.setting_info)
        self.simulator.load_code(self.code)
        self.cycle = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_cycle)
        self.initUI()

        self.timer.start(1000)

        self.ui.btn_setting.setEnabled(False)

    @pyqtSlot()
    def run_cycle(self):
        self.simulator.run_one_cycle(self.cycle)
        self.update_ui()
        if self.simulator.finish:
            self.timer.stop()
            self.ui.run_info.append('\nCode finished after cycle {}'.format(self.cycle))
        if self.cycle == self.stop:
            self.timer.stop()
            self.is_stop = True
            self.ui.btn_setting.setEnabled(True)
            return
        self.cycle += 1

    def update_ui(self):
        self.ui.run_info.clear()
        self.ui.run_info.append(self.simulator.info)
        self.ui.label_cycle.setText(str(self.cycle))

        for i in range(len(self.simulator.status_diagram)):
            for j in range(len(self.simulator.status_diagram[i])):
                if self.simulator.status_diagram[i][j] is not None:
                    self.ui.table_instructions.setItem(i, j+4, QTableWidgetItem(str(self.simulator.status_diagram[i][j])))
                    self.ui.table_instructions.item(i, j+4).setBackground(QColor(200,200,200))
                    self.ui.table_instructions.item(i, j+4).setForeground(QColor(255,0,0))


        units = self.simulator.get_all_units()
        self.ui.table_funcuints.clearContents()
        for i in range(len(units)):
            info = units[i].get_info()
            for j in range(len(info)):
                if info[j] is not None:
                    self.ui.table_funcuints.setItem(i, j, QTableWidgetItem(str(info[j])))


        regs = self.simulator.get_registers()

        for i in range(len(regs)):
            if regs[i].occupied:
                self.ui.table_registers.setItem(0, i, QTableWidgetItem(str(regs[i].funcunit)))
            else:
                self.ui.table_registers.setItem(0, i, QTableWidgetItem(''))


        regs = self.simulator.get_floatregisters()
        for i in range(len(regs)):
            if regs[i].occupied:
                self.ui.table_fregisters.setItem(0, i, QTableWidgetItem(str(regs[i].funcunit)))
            else:
                self.ui.table_fregisters.setItem(0, i, QTableWidgetItem(''))

    def clear(self):
        self.ui.run_info.clear()
        self.ui.table_funcuints.clearContents()
        self.ui.table_registers.clearContents()
        self.ui.table_instructions.clearContents()
        self.ui.table_fregisters.clearContents()
        self.ui.label_cycle.setText('0')
        self.ui.btn_pause.setText('pause')

    def pause(self):
        if self.is_start:
            if self.is_pause:
                self.continue_pipeline()
            else:
                self.timer.stop()
                self.is_pause = True
                self.ui.btn_pause.setText('continue')

    def continue_pipeline(self):
        self.timer.start(1000)
        self.is_pause = False
        self.ui.btn_pause.setText('pause')

    def stop(self):
        if self.is_start:
            self.timer.stop()
            self.clear()
            self.ui.btn_pause.setText('pause')
            self.ui.btn_setting.setEnabled(True)

    def loadFile(self):
        filename = QFileDialog.getOpenFileName(self)
        self.ui.run_info.append(str(filename))
        self.filename = filename[0]
        if self.filename:
            with open(self.filename) as file:
                self.code = file.read().strip()