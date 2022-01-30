import sqlite3
import sys
from main2 import Ui_MainWindow
from addEditCoffeeForm import Ui_MainWindow2

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import QTimer
lst = []
flag = False
h = ''


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QTimer()
        self.timer.start()
        self.timer.timeout.connect(self.display)
        self.ui.tableWidget.cellClicked.connect(self.aaa)
        self.ui.pushButton.clicked.connect(self.fl)

    def display(self):
        try:
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            result = cur.execute("SELECT * FROM инфа").fetchall()
            self.ui.tableWidget.setRowCount(len(result))
            self.ui.tableWidget.setColumnCount(len(result[0]))
            self.ui.tableWidget.setColumnWidth(0, 10)
            self.ui.tableWidget.setColumnWidth(1, 100)
            self.ui.tableWidget.setColumnWidth(2, 150)
            self.ui.tableWidget.setColumnWidth(3, 150)
            self.ui.tableWidget.setColumnWidth(4, 350)
            self.ui.tableWidget.setColumnWidth(6, 200)
            self.ui.tableWidget.setHorizontalHeaderLabels(('ID', 'Название сорта', 'Степень обжарки',
                                        'Молотый/в зернах', 'Описание вкуса', 'Цена (руб.)', 'Объем упаковки (г)'))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        except IndexError:
            pass

    def aaa(self):
        global flag, h, lst
        flag = True
        con = sqlite3.connect("release/coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM инфа").fetchall()
        row = self.ui.tableWidget.currentRow()
        for x in range(len(result[0])):
            value = self.ui.tableWidget.item(row, x)
            value = value.text()
            lst.append(value)

    def fl(self):
        global flag
        flag = False


class Clss(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        super().__init__()
        self.ui2 = Ui_MainWindow2()
        self.ui2.setupUi(self)
        self.ui2.pushButton.clicked.connect(self.ins)

    def ins(self):
        global flag
        global lst
        global h
        con = sqlite3.connect("release/coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM инфа").fetchall()
        if not flag:
            if self.ui2.lineEdit.text() and self.ui2.lineEdit_2.text() and self.ui2.lineEdit_3.text() and \
                    self.ui2.lineEdit_4.text() and self.ui2.lineEdit_5.text() and self.ui2.lineEdit_6.text():
                cur.execute("INSERT INTO инфа VALUES (?, ?, ?, ?, ?, ?, ?)", (len(result) + 1, self.ui2.lineEdit.text(),
                            self.ui2.lineEdit_2.text(), self.ui2.lineEdit_3.text(), self.ui2.lineEdit_4.text(),
                            self.ui2.lineEdit_5.text(), self.ui2.lineEdit_6.text()))
                self.close()
        else:
            if self.ui2.lineEdit.text() and self.ui2.lineEdit_2.text() and self.ui2.lineEdit_3.text() and \
                    self.ui2.lineEdit_4.text() and self.ui2.lineEdit_5.text() and self.ui2.lineEdit_6.text():
                s = "UPDATE инфа SET 'Название сорта' = '"
                s += self.ui2.lineEdit.text()
                s += "' WHERE ID = "
                s += h
                s1 = "UPDATE инфа SET 'Степень обжарки' = '"
                s1 += self.ui2.lineEdit_2.text()
                s1 += "' WHERE ID = "
                s1 += h
                s2 = "UPDATE инфа SET 'Молотый/в зернах' = '"
                s2 += self.ui2.lineEdit_3.text()
                s2 += "' WHERE ID = "
                s2 += h
                s3 = "UPDATE инфа SET 'Описание вкуса' = '"
                s3 += self.ui2.lineEdit_4.text()
                s3 += "' WHERE ID = "
                s3 += h
                s4 = "UPDATE инфа SET 'Цена (руб.)' = '"
                s4 += self.ui2.lineEdit_5.text()
                s4 += "' WHERE ID = "
                s4 += h
                s5 = "UPDATE инфа SET 'Объем упаковки (г)' = '"
                s5 += self.ui2.lineEdit_6.text()
                s5 += "' WHERE ID = "
                s5 += h
                cur.execute(s)
                cur.execute(s1)
                cur.execute(s2)
                cur.execute(s3)
                cur.execute(s4)
                cur.execute(s5)
                self.close()

        con.commit()
        con.close()
        self.ui2.lineEdit.setText("")
        self.ui2.lineEdit_2.setText("")
        self.ui2.lineEdit_3.setText("")
        self.ui2.lineEdit_4.setText("")
        self.ui2.lineEdit_5.setText("")
        self.ui2.lineEdit_6.setText("")

    def edit(self):
        global lst, h
        h = lst[0]
        self.ui2.lineEdit.setText(lst[1])
        self.ui2.lineEdit_2.setText(lst[2])
        self.ui2.lineEdit_3.setText(lst[3])
        self.ui2.lineEdit_4.setText(lst[4])
        self.ui2.lineEdit_5.setText(lst[5])
        self.ui2.lineEdit_6.setText(lst[6])
        lst = []

    def dele(self):
        self.ui2.lineEdit.setText("")
        self.ui2.lineEdit_2.setText("")
        self.ui2.lineEdit_3.setText("")
        self.ui2.lineEdit_4.setText("")
        self.ui2.lineEdit_5.setText("")
        self.ui2.lineEdit_6.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    yx = Clss()
    ex.ui.pushButton.clicked.connect(yx.show)
    ex.ui.pushButton.clicked.connect(yx.dele)
    ex.ui.tableWidget.cellClicked.connect(yx.show)
    ex.ui.tableWidget.cellClicked.connect(yx.edit)
    ex.show()
    sys.exit(app.exec())
