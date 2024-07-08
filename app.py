from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QScrollArea, QDoubleSpinBox, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, 
    QColorDialog, QLabel, QFileDialog
)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys, json, os
from pynput import keyboard
import threading

class SenaKps(QWidget):
    def __init__(self):
        super().__init__()
        # slots and threads(handle pynput listener)
        self.listener = KeyListener()
        self.listener.on_press_signal.connect(self.on_press)
        self.listener.on_release_signal.connect(self.on_release)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.start()
        #variable
        self.key_symbol = []
        self.key_name = []
        self.key_block_list = []
        self.key_symbol_list = []
        self.key_count_list = []
        self.token = True
        # load settings
        filePath, _ = QFileDialog.getOpenFileName(filter='JSON (*.json)')
        try:
            if filePath:
                jsonFile = open(filePath, 'r', encoding='utf-8')
                self.settings = json.load(jsonFile)
                for i in self.settings['keyEvent']:
                    self.key_symbol.append(i['keySymbol'])
                    self.key_name.append(i['key'])
            else:
                print('cancel loading file!')
                self.close()
        except:
            print('open file error!')
            self.close()
        #change key amount
        self.key_amount = len(self.key_symbol)
        self.counter = [0] * self.key_amount
        #load senakps file
        try:
            self.snakps_route, _ = QFileDialog.getOpenFileName(filter='SENAKPS FILE (*.senakps)')

            record = open(self.snakps_route, 'r', encoding='utf-8')
            tmp  = record.read()
            tmp = tmp.split('@')[1].split('\n')
            amount = {}
            for _ in tmp:
                if _ == 'keyClick' or _ == '':
                    continue
                _ = _.split((':'))
                amount[_[0]] = _[1]
                if _[0] in self.key_symbol:
                    self.counter[self.key_symbol.index(_[0])] = self.counter[self.key_symbol.index(_[0])] + int(_[1])
        except:
            print('senakps file is new or has error!')
            record.close()
        record.close()
        # def font size
        self.font_size = [1] * self.key_amount
        for index, values in enumerate(self.counter):
            self.font_size[index] = 26 - len(str(values))
        #mainwindow settings
        self.setObjectName("senaKPS")
        self.setWindowTitle('senaKPS')
        self.setWindowOpacity(self.settings['opacity'])
        self.resize(60*self.key_amount, 90)
        self.setFixedSize(60*self.key_amount, 90)
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
        hbox = QWidget(self)
        hbox.setGeometry(0,0,60*self.key_amount,90)
        css = f'background-color: {self.settings["color"]["backgroundColor"]}'
        hbox.setStyleSheet(css)
        h_layout = QHBoxLayout(hbox)
        h_layout.setContentsMargins(3, 5, 3, 5)

        for i in range(1,self.key_amount + 1):
            h_layout.addWidget(self.create_keyblock(i-1))
    #close windows event
    def closeEvent(self, event):
        record = open(self.snakps_route, 'w', encoding='utf-8')
        record.write('@keyClick\n')
        for index, symbol in enumerate(self.key_symbol):
            record.write(f'{symbol}:{str(self.counter[index])}\n')
        record.close()
        event.accept()

    def create_keyblock(self, symbol_index):
        container = QWidget(self)
        id_name = f'container{symbol_index}'
        css = f'''
        QWidget#{id_name}{{ border: 2px solid {self.settings["color"]["mainColor"]}; }}
        QWidget#{id_name} QLabel {{ font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]}; }}
        '''
        container.setObjectName(id_name)
        container.setStyleSheet(css)
        container_layout = QVBoxLayout(container)

        div_up = QLabel(self)
        div_up.setText(self.key_symbol[symbol_index])
        div_up.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(div_up)
        self.key_symbol_list.append(div_up)
        div_dw = QLabel(self)
        div_dw.setText(str(self.counter[symbol_index]))
        div_dw.setAlignment(Qt.AlignCenter)
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
            tmp_key = str()
            if hasattr(key, 'char'):
                tmp_key = key.char
            elif hasattr(key, 'name'):
                tmp_key = key.name
            print((tmp_key))
            if tmp_key in self.key_name:
                self.counter[self.key_name.index(tmp_key)] += 1
                if len(str(self.counter[self.key_name.index(tmp_key)])) > self.font_size[self.key_name.index(tmp_key)]:
                    self.font_size[self.key_name.index(tmp_key)] - 1
                css = f'font-size: {self.font_size[self.key_name.index(tmp_key)]}px; font-weight:bold; color: {self.settings["color"]["backgroundColor"]};'
                self.key_symbol_list[self.key_name.index(tmp_key)].setStyleSheet(css)
                self.key_count_list[self.key_name.index(tmp_key)].setStyleSheet(css)
                css = f'background-color: {self.settings["color"]["mainColor"]};'
                self.key_block_list[self.key_name.index(tmp_key)].setStyleSheet(css)
                self.key_count_list[self.key_name.index(tmp_key)].setText(str(self.counter[self.key_name.index(tmp_key)]))
            self.token = False

    @pyqtSlot(object)
    def on_release(self, key):
        tmp_key = str()
        if hasattr(key, 'char'):
            tmp_key = key.char
        elif hasattr(key, 'name'):
            tmp_key = key.name
        if tmp_key in self.key_name:
            self.key_symbol_list[self.key_name.index(tmp_key)].setStyleSheet(f'font-size: 25px; font-weight:bold; color: {self.settings["color"]["mainColor"]};')
            self.key_count_list[self.key_name.index(tmp_key)].setStyleSheet(f'font-size: {self.font_size[self.key_name.index(tmp_key)]}px; font-weight:bold; color: {self.settings["color"]["mainColor"]};')
            css = f'''QWidget#container{self.key_name.index(tmp_key)}{{ border: 2px solid {self.settings["color"]["mainColor"]}; background-color: {self.settings["color"]["backgroundColor"]}; }}'''
            self.key_block_list[self.key_name.index(tmp_key)].setStyleSheet(css)
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
    app = QApplication(sys.argv)
    mainwindow = SenaKps()
    mainwindow.show()
    sys.exit(app.exec_())