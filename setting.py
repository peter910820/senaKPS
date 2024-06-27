from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QSizePolicy, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys, json
from pynput import keyboard
import threading

class SenaKpsSetting(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        #mainwindow settings
        self.setObjectName("senaKPS_Setting")
        self.setWindowTitle('senaKPS-Setting')
        self.resize(355, 180)
        self.setFixedSize(355, 180)
        self.key_table = None
        self.table_index = 0
        self.ui()

    def ui(self):
        vbox = QtWidgets.QWidget(self)
        vbox.setGeometry(0, 0, 355, 180)
        self.v_layout = QtWidgets.QVBoxLayout(vbox)
        new_key = QPushButton('create new key', self)
        new_key.clicked.connect(self.new_key_click)
        self.v_layout.addWidget(new_key, alignment=Qt.AlignTop)

    def new_key_click(self):
        self.key_set = KeySet()
        self.key_set.accept_data.connect(self.accept_data)
        self.key_set.show()
        
    @pyqtSlot(str)
    def accept_data(self, key):
        if self.key_table:
            rows_end = self.key_table.rowCount()
            self.key_table.insertRow(rows_end)
        else:
            self.key_table = QTableWidget(1, 3)
            self.key_table.setHorizontalHeaderLabels(['symbol', 'key', 'remove'])

        symbol = QTableWidgetItem(key)
        key = QTableWidgetItem(key)
        remove = QPushButton('remove')
        remove.clicked.connect(self.remove_button_click)
        self.key_table.setItem(self.table_index, 0, symbol)
        self.key_table.setItem(self.table_index, 1, key)
        self.key_table.setCellWidget(self.table_index, 2, remove)
        self.v_layout.addWidget(self.key_table)
        self.table_index += 1

    def remove_button_click(self):
        print('哈哈我還沒做拉')

class KeySet(QtWidgets.QWidget):
    accept_data = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.listener = KeyListener()
        self.listener.on_press_signal.connect(self.on_press)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.start()

        self.key = ""

        self.setWindowTitle('key set')
        self.resize(300, 300)
        self.setFixedSize(300, 300)
        self.ui()

    def ui(self):
        vbox = QtWidgets.QWidget(self)
        vbox.setGeometry(0, 0, 300, 300)
        v_layout = QtWidgets.QVBoxLayout(vbox)
        self.key_show = QtWidgets.QLabel(self)
        self.key_show.setText('press any key')
        css = 'border: 2px solid black; font-size: 20px;'
        self.key_show.setStyleSheet(css)
        self.key_show.setAlignment(QtCore.Qt.AlignCenter)
        self.key_show.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v_layout.addWidget(self.key_show, 9)
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.ok_button_click)
        ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v_layout.addWidget(ok_button, 1)

    def ok_button_click(self):
        self.accept_data.emit(self.key)
        self.listener.stop()
        self.close()
        
    @pyqtSlot(object)
    def on_press(self, key):
        if hasattr(key, 'char'):
            print(key.char)
            self.key = key.char
            self.key_show.setText(key.char)
        if hasattr(key, 'name'):
            print(key.name)
            self.key = key.name
            self.key_show.setText(key.name)

class KeyListener(QObject):
    on_press_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.listener = keyboard.Listener(on_press=self.on_press)
    
    def start(self):
        self.listener.start()
        
    def stop(self):
         self.listener.stop()

    def on_press(self, key):
        self.on_press_signal.emit(key)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = SenaKpsSetting()
    mainwindow.show()
    sys.exit(app.exec_())