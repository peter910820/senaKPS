from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QScrollArea, QDoubleSpinBox, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, 
    QColorDialog, QLabel, QFileDialog
)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt

from pynput import mouse

import threading

from SenakpsModules.listener import MouseListener

class MouseWindow(QWidget):
    def __init__(self):
        super().__init__()
        # slots and threads(handle pynput listener)
        self.listener = MouseListener()
        self.listener.on_click_signal.connect(self.on_click)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.start()
        #variable
        self.key_block_list, self.key_symbol_list, self.key_count_list = [], [], []
        self.token = True
        #change key amount
        self.symbol = ['left', 'middle', 'right']
        self.key_amount = 3
        self.counter = [0] * 3
        self.tmp = 0
        #mainwindow settings
        self.setObjectName("BetaTest")
        self.setWindowTitle('BetaTest')
        self.setWindowOpacity(0.9)
        self.resize(100*self.key_amount, 90)
        self.setFixedSize(100*self.key_amount, 90)
        self.ui()

    def ui(self) -> None:
        hbox = QWidget(self)
        hbox.setGeometry(0,0,100*self.key_amount,90)
        css = f'background-color: "black"'
        hbox.setStyleSheet(css)
        h_layout = QHBoxLayout(hbox)
        h_layout.setContentsMargins(3, 5, 3, 5)

        for i in range(1,self.key_amount + 1):
            h_layout.addWidget(self.create_keyblock(i-1))

    def create_keyblock(self, symbol_index) -> object:
        container = QWidget(self)
        id_name = f'container{symbol_index}'
        css = f'''
        QWidget#{id_name}{{ border: 2px solid "pink"; }}
        QWidget#{id_name} QLabel {{ font-size: 25px; font-weight:bold; color: "pink"; }}
        '''
        container.setObjectName(id_name)
        container.setStyleSheet(css)
        container_layout = QVBoxLayout(container)

        div_up = QLabel(self)
        div_up.setText(self.symbol[symbol_index])
        div_up.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(div_up)
        self.key_symbol_list.append(div_up)
        div_dw = QLabel(self)
        div_dw.setText("0")
        div_dw.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(div_dw)

        self.key_count_list.append(div_dw)
        self.key_block_list.append(container)
        return container
    
    #close windows event
    def closeEvent(self, event):
        self.listener.stop()
        self.close()

    @pyqtSlot(object, object)
    def on_click(self, button, pressed) -> None:
        if pressed:
            if button == mouse.Button.left:
                self.tmp = 0
            elif button == mouse.Button.middle:
                self.tmp = 1
            elif button == mouse.Button.right:
                self.tmp = 2
            else:
                print('Exception!!')
            self.counter[self.tmp] += 1
            css = f'font-size: 25px; font-weight:bold; color: "black"';
            self.key_symbol_list[self.tmp].setStyleSheet(css)
            self.key_count_list[self.tmp].setStyleSheet(css)
            css = f'background-color: "pink";'
            self.key_block_list[self.tmp].setStyleSheet(css)
            self.key_count_list[self.tmp].setText(str(self.counter[self.tmp]))
        else: #released
            self.key_symbol_list[self.tmp].setStyleSheet(f'font-size: 25px; font-weight:bold; color: "pink";')
            self.key_count_list[self.tmp].setStyleSheet(f'font-size: 25px; font-weight:bold; color: "pink";')
            css = f'''QWidget#container{self.tmp}{{ border: 2px solid "pink"; background-color: "black"; }}'''
            self.key_block_list[self.tmp].setStyleSheet(css)