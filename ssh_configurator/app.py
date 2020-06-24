from __future__ import absolute_import
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
        self.model = QStandardItemModel(self)
        self.init_table()
        self.btn_add_row.clicked.connect(self.add_rows)
        self.btn_reset_table.clicked.connect(self.init_table)

    def init_table(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['subnet/ip', 'username', 'command'])
        self.model.setRowCount(18)
        self.table.setModel(self.model)

    def add_rows(self):
        rows = self.model.rowCount()
        self.model.setRowCount(rows + self.num_rows.value())

    def getfile(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open csv', QDir.rootPath(), '*.csv')
        try:
            self.readCsv(path)
        except Exception as error:
            print(error)

    def readCsv(self, fileName):
        self.model.clear()
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            print(csv_reader)
            for row in csv_reader:

                items = [QStandardItem(field) for field in row]

                self.model.appendRow(items)
            self.table.horizontalHeader()

    def execute_commands(self):
        rows = self.model.rowCount()
        for i in range(0, rows):
            try:
                host = self.model.item(i, 0)
                user = self.model.item(i, 1)
                cmd = self.model.item(i, 2)
                if host and user and cmd:
                    host = host.text()
                    user = user.text()
                    cmd = cmd.text()

                    self.log.appendPlainText(f"{host}, {user}, {cmd}")
                    execute_with_subnet(subnet=host, user=user, password=self.line_password.text(), cmd=cmd, log=self.log)
            except Exception as error:
                print(error)

    def start_thread(self):
        p = Thread(target=self.execute_commands)
        p.start()


def main():
   app = QApplication(sys.argv)
   ex = Application()
   ex.show()
   sys.exit(app.exec_())


if __name__ == "__main__":
    main()
