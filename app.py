from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys
from pynput import keyboard

class SenaKps(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("senaKPS")
        self.setWindowTitle('senaKPS')
        self.setWindowOpacity(0.8)
        self.resize(355, 90)
        self.setFixedSize(355, 90)
        
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) #無邊框

        self.div_arr = []
        self.ui()

        self.counter = 0
        self.listener = None
        self.key_listener()

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap('transparent_image.png')

    #     pixmap = pixmap.scaled(self.size())

    #     painter.drawPixmap(self.rect(), pixmap)

    def ui(self):
        hbox = QtWidgets.QWidget(self)
        hbox.setGeometry(0,0,355,90)
        h_layout = QtWidgets.QHBoxLayout(hbox)
        hbox.setObjectName('main')
        hbox.setStyleSheet('Qwidget#main { background-image: url("http://ustrack.amusecraft.com/koikake/img_sub/cg_zoom/cg03.jpg") };')
        h_layout.setContentsMargins(3, 5, 3, 5)

        for i in range(1,7):
            key_block = self.create_keyblock(str(i))
            h_layout.addWidget(key_block)

    def create_keyblock(self, t):
        container = QtWidgets.QWidget(self)
        container.setObjectName("container")
        container.setStyleSheet('QWidget#container { border: 2px solid #9999ff; }')
        container_layout = QtWidgets.QVBoxLayout(container)

        div_up = QtWidgets.QLabel(self)
        div_up.setText('↵')
        div_up.setStyleSheet('font-size: 25px; font-weight:bold; color: #9999ff')
        div_up.setAlignment(QtCore.Qt.AlignCenter)
        container_layout.addWidget(div_up)
        div_dw = QtWidgets.QLabel(self)
        div_dw.setText(str(0))
        div_dw.setStyleSheet('font-size: 25px; font-weight:bold; color: #9999ff ')
        div_dw.setAlignment(QtCore.Qt.AlignCenter)
        self.div_arr.append(div_dw)
        container_layout.addWidget(div_dw)
        return container
    
    def key_listener(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
         self.counter += 1
         for arr in self.div_arr:
            arr.setText(str(self.counter))
         print(f'Pressed key: {key}')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = SenaKps()
    mainwindow.show()
    sys.exit(app.exec_())