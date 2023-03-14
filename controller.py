'''
    controller
'''

from view import View
from model import Model
import sys

class Controller():
    def __init__(self):
        source_path = "test/test.mp4"
        view = View(source_path)
        model = Model(back=10,forward=30)

        self.window = view.window
        self.w_player = view.player

        self.m_player = model.player

        self.set_button_connections()

        self.w_player.play()

        self.window.show()
        
        sys.exit(self.window.app.exec())
    
    def set_button_connections(self):
        ms_back = self.m_player.ms_back
        self.window.btnBack.clicked.connect(lambda: self.w_player.go_back(ms_back))
        self.window.tool_bar.addWidget(self.window.btnBack)


        ms_forward = self.m_player.ms_forward
        print(ms_back,ms_forward)
        self.window.btnForward.clicked.connect(lambda: self.w_player.go_forward(ms_forward))
        self.window.tool_bar.addWidget(self.window.btnForward)


if __name__ == '__main__':
    c = Controller()