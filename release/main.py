import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sqlite3
from UI.ui_main import Ui_main
from UI.addEditCoffeeForm import Ui_addEditCoffeeForm


class Espresso(QMainWindow, Ui_main):
    def __init__(self):
        super().__init__()
        self.Window = None
        self.setupUi(self)
        con = sqlite3.connect("data/coffee.sqlite")
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
        self.add_change_window.clicked.connect(self.show_add_change_window)

    def show_add_change_window(self):
        self.close()
        self.Window = AddChange()
        self.Window.show()


class AddChange(QMainWindow, Ui_addEditCoffeeForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Window = None
        self.add_btn.clicked.connect(self.add_func)
        self.change_btn.clicked.connect(self.change_func)
        self.back_btn.clicked.connect(self.back_func)

    def add_func(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        count = cur.execute(f"""SELECT ID FROM infoffee""").fetchall()
        if len(count) == 0:
            id_number = 1
        else:
            id_number = count[-1][0] + 1
        cur.execute(f"""INSERT INTO infoffee 
                (ID, name, stepen, condition, taste, price, volume)
                VALUES 
                (?, ?, ?, ?, ?, ?, ?)""", (id_number, self.name_line.text(), self.stepen_line.text(),
                                           self.condition_line.text(), self.taste_line.text(), self.price_line.text(),
                                           self.volume_line.text()))
        con.commit()
        con.close()

    def change_func(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        cur.execute(f"""UPDATE infoffee
                        SET name = ?, stepen = ?, condition = ?, taste = ?, price = ?, volume = ?
                        WHERE ID = ?""", (self.name_change.text(),
                                          self.stepen_change.text(), self.condition_change.text(),
                                          self.taste_change.text(), self.price_change.text(),
                                          self.volume_change.text(), int(self.which_change.text())))
        con.commit()
        con.close()

    def back_func(self):
        self.close()
        self.Window = Espresso()
        self.Window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec())
