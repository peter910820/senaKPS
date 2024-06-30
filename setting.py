from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QScrollArea, QDoubleSpinBox, 
    QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, 
    QColorDialog, QLabel, QFileDialog
)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
import sys, json

from pynput import keyboard
import threading

from SenakpsModules import symbol_translate

class SenaKpsSetting(QWidget):
    def __init__(self):
        super().__init__()
        #mainwindow settings
        self.setObjectName("senaKPS_Setting")
        self.setWindowTitle('senaKPS Setting')
        self.resize(335, 300)
        self.setFixedSize(335, 300)
        self.table_index = 0

        self.key_block_index = 0

        self.key_block_list, self.key_block_symbol_list, self.key_block_key_list = {}, {}, {}

        self.mainColor, self.backgroundColor = 'pink', 'black'

        self.settings = None

        self.symbol_table = SymbolTranslate().get_symbol_table()
        self.ui()
        
    def ui(self):
        vbox = QWidget(self)
        vbox.setGeometry(0, 0, 335, 300)
        self.v_layout = QVBoxLayout(vbox)

        hbox_settings = QWidget(self)
        hbox_settings_layout = QHBoxLayout(hbox_settings)
        hbox_settings_layout.setContentsMargins(0, 0, 0, 0)

        load_settings = QPushButton('load settings', self)
        load_settings.clicked.connect(self.load_settings_click)
        save_settings = QPushButton('save settings', self)
        save_settings.clicked.connect(self.save_settings_click)
        hbox_settings_layout.addWidget(load_settings)
        hbox_settings_layout.addWidget(save_settings)

        new_key = QPushButton('create new key', self)
        new_key.clicked.connect(self.new_key_click)
        
        self.create_key_area()

        hbox = QWidget(self)
        h_layout = QHBoxLayout(hbox)
        h_layout.setContentsMargins(0, 0, 0, 0)
        backgroundColor = QPushButton('backgroundColor', self)
        backgroundColor.clicked.connect(lambda: self.color_click(False))
        self.backgroundColor_color = QLabel(self)
        self.backgroundColor_color.setStyleSheet(f'background-color: {self.backgroundColor}')
        mainColor = QPushButton('mainColor', self)
        mainColor.clicked.connect(lambda: self.color_click(True))
        self.mainColor_color = QLabel(self)
        self.mainColor_color.setStyleSheet(f'background-color: {self.mainColor}')
        
        backgroundColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.backgroundColor_color.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mainColor_color.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_layout.addWidget(backgroundColor, 4)
        h_layout.addWidget(self.backgroundColor_color, 1)
        h_layout.addWidget(mainColor, 4)
        h_layout.addWidget(self.mainColor_color, 1)
        #opacity block
        self.opacity = QDoubleSpinBox(self)
        self.opacity.setDecimals(1)
        self.opacity.setRange(0, 1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(1.0)

        main_start = QPushButton('OK', self)
        main_start.clicked.connect(self.main_start_click)
        main_start.setEnabled(False)

        self.v_layout.addWidget(hbox_settings)
        self.v_layout.addWidget(new_key, alignment=Qt.AlignTop)
        self.v_layout.addWidget(self.scroll_area)
        self.v_layout.addWidget(hbox)
        self.v_layout.addWidget(self.opacity)
        self.v_layout.addWidget(main_start)

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

    def load_settings_click(self):
        filePath, _ = QFileDialog.getOpenFileName(filter='JSON (*.json)')
        try:
            if filePath:
                settings_file = open(filePath, 'r', encoding='utf-8')
                self.settings = json.load(settings_file)
                settings_file.close()
                print(self.settings)
                self.mapping()
            else:
                print('cancel loading file!')
        except:
            print('open file error!')

    def save_settings_click(self):
        filePath, _ = QFileDialog.getSaveFileName(filter='JSON (*.json)')
        if filePath:
            setting_file = open(filePath, 'w', encoding='utf-8')
            tmp = {
                "keyEvent":[],
                "color": {
                    "backgroundColor": f"{self.backgroundColor}",
                    "mainColor": f"{self.mainColor}"
                },
                "opacity": round(self.opacity.value(), 1)
            }
            for keys, values in self.key_block_symbol_list.items():
                tmp['keyEvent'].append({
                    "keySymbol": values.text(),
                    "key": self.key_block_key_list[keys].text()
                })
            y = json.dumps(tmp)
            setting_file.write(y)
            setting_file.close()
            save_message = QMessageBox(self)
            save_message.information(self, 'message', 'save complete!')
        else:
            print('cancel saving file!')

    def mapping(self):
        try:
            self.opacity.setValue(self.settings['opacity'])
            self.backgroundColor = self.settings['color']['backgroundColor']
            self.mainColor = self.settings['color']['mainColor']
            self.backgroundColor_color.setStyleSheet(f'background-color: {self.backgroundColor}')
            self.mainColor_color.setStyleSheet(f'background-color: {self.mainColor}')

            self.key_block_index = 0
            for index in self.key_block_list:
                self.key_table_layout.removeWidget(self.key_block_list[index])
                self.key_block_list[index].deleteLater()
            self.key_block_list, self.key_block_symbol_list, self.key_block_key_list = {}, {}, {}
            
            for i in self.settings['keyEvent']:
                index = self.key_block_index
                key_block = QWidget(self)
                key_block_layout = QHBoxLayout(key_block)
                key_block_layout.setContentsMargins(0, 0, 0, 0)
                key_block_symbol = QLabel(self)
                key_block_symbol.setText(i['keySymbol'])
                key_block_key = QLabel(self)
                key_block_key.setText(i['key'])
                key_block_remove = QPushButton('remove')
                key_block_remove.clicked.connect(lambda state, idx=index: self.remove_button_click(str(idx)))
                key_block_symbol.setAlignment(Qt.AlignCenter)
                key_block_key.setAlignment(Qt.AlignCenter)
                key_block_layout.addWidget(key_block_symbol)
                key_block_layout.addWidget(key_block_key)
                key_block_layout.addWidget(key_block_remove)
                key_block.setFixedHeight(20)

                self.key_block_symbol_list[str(index)] = key_block_symbol
                self.key_block_key_list[str(index)] = key_block_key
                self.key_block_list[str(index)] = key_block

                self.key_table_layout.addWidget(key_block)
                self.scroll_area.setWidget(self.key_table)

                self.key_block_index += 1
        except:
            print('format error!')

    def main_start_click(self): pass

    def color_click(self, judge):
        color = QColorDialog().getColor()
        print(color.name())
        if judge:
            self.mainColor_color.setStyleSheet(f'background-color: {color.name()}')
            self.mainColor = color.name()
        else:
            self.backgroundColor_color.setStyleSheet(f'background-color: {color.name()}')
            self.backgroundColor = color.name()

    @pyqtSlot(str)
    def accept_data(self, key):
        index = self.key_block_index
        key_block = QWidget(self)
        key_block_layout = QHBoxLayout(key_block)
        key_block_layout.setContentsMargins(0, 0, 0, 0)
        key_block_symbol = QLabel(self)
        if key in self.symbol_table:
            key_block_symbol.setText(self.symbol_table[key])
        else:
            key_block_symbol.setText(key)
        key_block_key = QLabel(self)
        key_block_key.setText(key)
        key_block_remove = QPushButton('remove')
        key_block_remove.clicked.connect(lambda: self.remove_button_click(str(index)))
        key_block_symbol.setAlignment(Qt.AlignCenter)
        key_block_key.setAlignment(Qt.AlignCenter)
        key_block_layout.addWidget(key_block_symbol)
        key_block_layout.addWidget(key_block_key)
        key_block_layout.addWidget(key_block_remove)
        key_block.setFixedHeight(20)

        self.key_block_symbol_list[str(index)] = key_block_symbol
        self.key_block_key_list[str(index)] = key_block_key
        self.key_block_list[str(index)] = key_block

        self.key_table_layout.addWidget(key_block)
        self.scroll_area.setWidget(self.key_table)

        self.key_block_index += 1

    def remove_button_click(self, index):
        self.key_table_layout.removeWidget(self.key_block_list[index])
        self.key_block_list[index].deleteLater()
        self.key_block_list.pop(index, None)
        self.key_block_symbol_list.pop(index, None)
        self.key_block_key_list.pop(index, None)
        print(f'key_block_list size: {len(self.key_block_list)}')

class SymbolTranslate():
    def __init__(self) -> None:
        symbol_table_file = open('./symbol-file.json', 'r', encoding='utf-8')
        self.symbol_table = json.load(symbol_table_file)
        print(self.symbol_table)
        symbol_table_file.close()

    def get_symbol_table(self):
        return self.symbol_table

class KeySet(QWidget):
    accept_data = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.listener = KeyListener()
        self.listener.on_press_signal.connect(self.on_press)
        self.listener_thread = threading.Thread(target=self.listener.start)
        self.listener_thread.start()

        self.key = ''

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