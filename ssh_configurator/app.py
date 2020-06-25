from __future__ import absolute_import

import time

from ssh_configurator import Ui_MainWindow
from device_config.device_config import execute_with_subnet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import csv
from threading import Thread


class Application(Ui_MainWindow, QMainWindow):

    def __init__(self, parent=None):
        super(Application, self).__init__(parent)
        self.setupUi(self)
        self.actionImport.triggered.connect(self.getfile)
        self.start.clicked.connect(self.start_thread)
        self.init_table(18)
        self.btn_add_row.clicked.connect(self.add_rows)
        self.btn_reset_table.clicked.connect(self.init_table)

    def init_table(self, row_num):
        # self.model.clear()
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['subnet/ip', 'username', 'command', 'password'])
        self.table.setRowCount(row_num)
        rows = self.table.rowCount()
        for i in range(rows):
            self.add_pwd_widget(i)

    def add_rows(self):
        rows = self.table.rowCount()
        self.table.setRowCount(rows + self.num_rows.value())
        for i in range(rows, rows + self.num_rows.value()):
            self.add_pwd_widget(i)

    def getfile(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open csv', QDir.rootPath(), '*.csv')
        try:
            self.readCsv(path)
        except Exception as error:
            print(error)

    def add_pwd_widget(self, row, data=None):
        pwd = QLineEdit()
        pwd.setEchoMode(QLineEdit.Password)
        self.table.setCellWidget(row, 3, pwd)
        if data:
            pwd.setText(data)

    def readCsv(self, fileName):
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            rows = [row for row in csv_reader]
            self.init_table(len(rows))
            self.import_data(rows)

    def import_data(self, rows):

        for inx, row in enumerate(rows):
            for i, col in enumerate(row):
                cellinfo = QTableWidgetItem(col)
                self.table.setItem(inx, i, cellinfo)
                self.add_pwd_widget(inx, col)

        self.table.horizontalHeader()

    def execute_commands(self):
        rows = self.table.rowCount()
        password = self.line_password.text()
        for i in range(0, rows):
            try:
                host = self.table.item(i, 0)
                user = self.table.item(i, 1)
                cmd = self.table.item(i, 2)
                pwd = self.table.cellWidget(i, 3)

                if host and user and cmd:
                    host = host.text()
                    user = user.text()
                    cmd = cmd.text()
                    if self.include_password.isChecked() and pwd:
                        password = pwd.text()
                    self.log.appendPlainText(f"{host}, {user}, {cmd}")
                    execute_with_subnet(subnet=host, user=user, password=password, cmd=cmd, log=self.log)
            except Exception as error:
                self.log.appendPlainText(str(error))

    def start_thread(self):
        p = Thread(target=self.execute_commands)
        p.start()
        p.is_alive()
        p.join(1)


def main():
   app = QApplication(sys.argv)
   ex = Application()
   ex.show()
   sys.exit(app.exec_())


if __name__ == "__main__":
    main()
