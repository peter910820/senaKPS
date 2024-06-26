from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys, json
from pynput import keyboard
import threading

class SenaKps(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # slots and threads(handle pynput listener)
        self.listener = KeyListener()
        self.listener.on_press_signal.connect(self.on_press)
        self.listener.on_release_signal.connect(self.on_release)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.start()
        #variable
        self.key_amount = 6
        self.counter = [0] * self.key_amount 
        self.key_symbol = []
        self.key_name = []
        self.key_block_list = []
        self.key_symbol_list = []
        self.key_count_list = []
        self.token = True
        # load settings
        jsonFile = open('./settings.json', 'r', encoding='utf-8')
        self.settings = json.load(jsonFile)
        for i in self.settings['keyEvent']:
            self.key_symbol.append(i['keySymbol'])
            self.key_name.append(i['key'])
        #mainwindow settings
        self.setObjectName("senaKPS")
        self.setWindowTitle('senaKPS')
        self.setWindowOpacity(self.settings['opacity'])
        self.resize(355, 90)
        self.setFixedSize(355, 90)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True) #預設透明
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #無邊框
        #create ui
        self.ui()

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap('cover.png')

    #     pixmap = pixmap.scaled(self.size())

    #     painter.drawPixmap(self.rect(), pixmap)

    def ui(self):
        hbox = QtWidgets.QWidget(self)
        hbox.setGeometry(0,0,355,90)
        css = f'background-color: {self.settings["color"]["backgroundColor"]}'
        hbox.setStyleSheet(css)
        h_layout = QtWidgets.QHBoxLayout(hbox)
        h_layout.setContentsMargins(3, 5, 3, 5)

        for i in range(1,self.key_amount + 1):
            key_block = self.create_keyblock(i-1)
            h_layout.addWidget(key_block)

    def create_keyblock(self, symbol_index):
        container = QtWidgets.QWidget(self)
        id_name = f'container{symbol_index}'
        css = f'''
        QWidget#{id_name}{{ border: 2px solid {self.settings["color"]["mainColor"]}; }}
        QWidget#{id_name} QLabel {{ font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]}; }}
        '''
        container.setObjectName(id_name)
        container.setStyleSheet(css)
        container_layout = QtWidgets.QVBoxLayout(container)

        div_up = QtWidgets.QLabel(self)
        div_up.setText(self.key_symbol[symbol_index])
        div_up.setAlignment(QtCore.Qt.AlignCenter)
        container_layout.addWidget(div_up)
        self.key_symbol_list.append(div_up)
        div_dw = QtWidgets.QLabel(self)
        div_dw.setText(str(0))
        div_dw.setAlignment(QtCore.Qt.AlignCenter)
        container_layout.addWidget(div_dw)

        self.key_count_list.append(div_dw)
        self.key_block_list.append(container)
        return container
    
    def key_listener(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    @pyqtSlot(object)
    def on_press(self, key):
        if self.token == True:
            if hasattr(key, 'char'):
                print((key.char))
                if key.char in self.key_name:
                    self.counter[self.key_name.index(key.char)] += 1
                    css = f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["backgroundColor"]};'
                    self.key_symbol_list[self.key_name.index(key.char)].setStyleSheet(css)
                    self.key_count_list[self.key_name.index(key.char)].setStyleSheet(css)
                    css = f'background-color: {self.settings["color"]["mainColor"]};'
                    self.key_block_list[self.key_name.index(key.char)].setStyleSheet(css)
                    self.key_count_list[self.key_name.index(key.char)].setText(str(self.counter[self.key_name.index(key.char)]))
            if hasattr(key, 'name'):
                print(key.name)
                if key.name in self.key_name:
                    self.counter[self.key_name.index(key.name)] += 1
                    css = f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["backgroundColor"]};'
                    self.key_symbol_list[self.key_name.index(key.name)].setStyleSheet(css)
                    self.key_count_list[self.key_name.index(key.name)].setStyleSheet(css)
                    css = f'background-color: {self.settings["color"]["mainColor"]};'
                    self.key_block_list[self.key_name.index(key.name)].setStyleSheet(css)
                    self.key_count_list[self.key_name.index(key.name)].setText(str(self.counter[self.key_name.index(key.name)]))
            self.token = False

    @pyqtSlot(object)
    def on_release(self, key):
        if hasattr(key, 'char'):
            if key.char in self.key_name:
                self.key_symbol_list[self.key_name.index(key.char)].setStyleSheet(f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]};')
                self.key_count_list[self.key_name.index(key.char)].setStyleSheet(f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]};')
                css = f'''QWidget#container{self.key_name.index(key.char)}{{ border: 2px solid {self.settings["color"]["mainColor"]}; background-color: {self.settings["color"]["backgroundColor"]}; }}'''
                self.key_block_list[self.key_name.index(key.char)].setStyleSheet(css)
        if hasattr(key, 'name'):
            if key.name in self.key_name:
                self.key_symbol_list[self.key_name.index(key.name)].setStyleSheet(f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]};')
                self.key_count_list[self.key_name.index(key.name)].setStyleSheet(f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]};')
                css = f'''QWidget#container{self.key_name.index(key.name)}{{ border: 2px solid {self.settings["color"]["mainColor"]}; background-color: {self.settings["color"]["backgroundColor"]}; }}'''
                self.key_block_list[self.key_name.index(key.name)].setStyleSheet(css)
        self.token = True

class KeyListener(QObject):
    on_press_signal = pyqtSignal(object)
    on_release_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
    
    def start(self):
        self.listener.start()
    
    def on_press(self, key):
        self.on_press_signal.emit(key)

    def on_release(self, key):
        self.on_release_signal.emit(key)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = SenaKps()
    mainwindow.show()
    sys.exit(app.exec_())