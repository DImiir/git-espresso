import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt6 import uic
import sqlite3


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        from_db = cur.execute("""SELECT * FROM infoffee""").fetchall()
        con.close()
        self.table.setRowCount(len(from_db))
        self.table.setColumnCount(7)
        for i, elem in enumerate(from_db):
            for j in range(len(elem)):
                self.table.setItem(i, j, QTableWidgetItem(str(elem[j])))
        self.table.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                                              'Описание вкуса', 'Цена', 'Объём упаковки'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
