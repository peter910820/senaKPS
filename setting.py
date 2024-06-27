from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QScrollArea, QDoubleSpinBox, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, 
    QColorDialog, QLabel
)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys
from pynput import keyboard
import threading

class SenaKpsSetting(QWidget):

    def __init__(self):
        super().__init__()
        #mainwindow settings
        self.setObjectName("senaKPS_Setting")
        self.setWindowTitle('senaKPS Setting')
        self.resize(335, 300)
        self.setFixedSize(335, 300)
        self.table_index = 0
        self.ui()

    def ui(self):
        vbox = QWidget(self)
        vbox.setGeometry(0, 0, 335, 300)
        self.v_layout = QVBoxLayout(vbox)
        new_key = QPushButton('create new key', self)
        new_key.clicked.connect(self.new_key_click)
        
        self.create_key_area()

        hbox = QWidget(self)
        h_layout = QHBoxLayout(hbox)
        h_layout.setContentsMargins(0, 0, 0, 0)
        backgroundColor = QPushButton('backgroundColor', self)
        backgroundColor.clicked.connect(lambda: self.color_click(False))
        self.backgroundColor_color = QLabel(self)
        self.backgroundColor_color.setStyleSheet('background-color: white')
        mainColor = QPushButton('mainColor', self)
        mainColor.clicked.connect(lambda: self.color_click(True))
        self.mainColor_color = QLabel(self)
        self.mainColor_color.setStyleSheet('background-color: white')
        backgroundColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.backgroundColor_color.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mainColor_color.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_layout.addWidget(backgroundColor, 4)
        h_layout.addWidget(self.backgroundColor_color, 1)
        h_layout.addWidget(mainColor, 4)
        h_layout.addWidget(self.mainColor_color, 1)

        opacity = QDoubleSpinBox(self)
        opacity.setDecimals(1)
        opacity.setRange(0, 1)
        opacity.setSingleStep(0.1)
        opacity.setValue(1.0)

        ok_key = QPushButton('OK', self)
        ok_key.clicked.connect(self.ok_key_click)

        self.v_layout.addWidget(new_key, alignment=Qt.AlignTop)
        self.v_layout.addWidget(self.scroll_area)
        self.v_layout.addWidget(hbox)
        self.v_layout.addWidget(opacity)
        self.v_layout.addWidget(ok_key)

    def create_key_area(self):
        self.key_table = QWidget(self)
        self.key_table_layout = QVBoxLayout(self.key_table)
        self.key_table_layout.setAlignment(Qt.AlignTop)

        key_block = QWidget(self)
        key_block_layout = QHBoxLayout(key_block)
        key_block_layout.setContentsMargins(0, 0, 0, 0)
        key_block_symbol = QLabel(self)
        key_block_symbol.setText('Symbol')
        key_block_key = QLabel(self)
        key_block_key.setText('Key')
        key_block_remove = QLabel(self)
        key_block_remove.setText('Remove')
        key_block_symbol.setAlignment(Qt.AlignCenter)
        key_block_key.setAlignment(Qt.AlignCenter)
        key_block_remove.setAlignment(Qt.AlignCenter)
        key_block_layout.addWidget(key_block_symbol, alignment=Qt.AlignTop)
        key_block_layout.addWidget(key_block_key, alignment=Qt.AlignTop)
        key_block_layout.addWidget(key_block_remove, alignment=Qt.AlignTop)
        key_block.setFixedHeight(20)

        self.scroll_area = QScrollArea()
        self.key_table_layout.addWidget(key_block)
        self.scroll_area.setWidget(self.key_table)
        self.scroll_area.setWidgetResizable(True)

    def new_key_click(self):
        self.key_set = KeySet()
        self.key_set.accept_data.connect(self.accept_data)
        self.key_set.show()

    def ok_key_click(self):
        pass

    def color_click(self, judge):
        color = QColorDialog().getColor()
        print(color.name())
        if judge:
            self.mainColor_color.setStyleSheet(f'background-color: {color.name()}')
        else:
            self.backgroundColor_color.setStyleSheet(f'background-color: {color.name()}')

        
    @pyqtSlot(str)
    def accept_data(self, key):
        key_block = QWidget(self)
        key_block_layout = QHBoxLayout(key_block)
        key_block_layout.setContentsMargins(0, 0, 0, 0)
        key_block_symbol = QLabel(self)
        key_block_symbol.setText(key)
        key_block_key = QLabel(self)
        key_block_key.setText(key)
        key_block_remove = QPushButton('remove')
        key_block_symbol.setAlignment(Qt.AlignCenter)
        key_block_key.setAlignment(Qt.AlignCenter)
        key_block_layout.addWidget(key_block_symbol)
        key_block_layout.addWidget(key_block_key)
        key_block_layout.addWidget(key_block_remove)
        key_block.setFixedHeight(20)

        self.key_table_layout.addWidget(key_block)
        self.scroll_area.setWidget(self.key_table)

    def remove_button_click(self):
        print('哈哈我還沒做拉')

class KeySet(QWidget):
    accept_data = pyqtSignal(str)

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
        vbox = QWidget(self)
        vbox.setGeometry(0, 0, 300, 300)
        v_layout = QVBoxLayout(vbox)
        self.key_show = QLabel(self)
        self.key_show.setText('press any key')
        css = 'border: 2px solid black; font-size: 20px;'
        self.key_show.setStyleSheet(css)
        self.key_show.setAlignment(Qt.AlignCenter)
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
    app = QApplication(sys.argv)
    mainwindow = SenaKpsSetting()
    mainwindow.show()
    sys.exit(app.exec_())