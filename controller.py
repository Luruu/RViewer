'''
    controller
'''

from view import View
from PySide6.QtCore import QRunnable, Slot, QThreadPool

class Controller():
    def __init__(self):
        source_path = "test/test.mp4"
        self.view = View(source_path)

if __name__ == '__main__':
    c = Controller()