from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt

from pynput import keyboard, mouse

class SettingListener(QObject):
    on_press_signal = pyqtSignal(object)
    
    def __init__(self) -> None:
        super().__init__()
        self.listener = keyboard.Listener(on_press=self.on_press)
    
    def start(self) -> None:
        self.listener.start()
        
    def stop(self) -> None:
        self.listener.stop()

    def on_press(self, key) -> None:
        self.on_press_signal.emit(key)

class MainListener(QObject):
    on_press_signal = pyqtSignal(object)
    on_release_signal = pyqtSignal(object)
    
    def __init__(self) -> None:
        super().__init__()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
    
    def start(self) -> None:
        self.listener.start()
        
    def stop(self) -> None:
        self.listener.stop()

    def on_press(self, key) -> None:
        self.on_press_signal.emit(key)

    def on_release(self, key) -> None:
        self.on_release_signal.emit(key)

class MouseListener(QObject):
    on_click_signal = pyqtSignal(object, object)

    def __init__(self) -> None:
        super().__init__()
        self.listener = mouse.Listener(on_click=self.on_click)

    def start(self) -> None:
        self.listener.start()
        
    def stop(self) -> None:
        self.listener.stop()

    def on_click(self, x, y, button, pressed) -> None:
        self.on_click_signal.emit(button, pressed)