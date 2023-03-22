'''
    controller
'''

from view import View
from model import Model
import sys

class Controller():
    def __init__(self):
        source_path = "test/test_sub.mkv"

        view = View(source_path)
        model = Model(back=10,forward=30)

        self.window = view.window
        self.w_player = view.player

        self.m_player = model.player

        self.set_view_connections()
        
        
        self.play_pause()
        self.w_player.parse_media()

        print(self.w_player.vlc_player.get_full_title_descriptions())
        
        print("[test] n_subtitles:", self.w_player.get_sub_count())
        print("[est] get_subtitles:", self.w_player.get_sub())
        
        self.window.show()
        
        sys.exit(self.window.app.exec())
    

    def play_pause(self):
        if self.w_player.is_playing():
            self.w_player.pause()
            self.window.play_pause_action.setIcon(self.window.icon_play)
        else:
            self.w_player.play()
            self.window.play_pause_action.setIcon(self.window.icon_pause)

    def changeSpeedVideo(self):
        new_speed = self.window.speed_slider.value() / 5
        self.window.label_speed.setText(" " + str(new_speed) + "x")
        self.w_player.set_rate(new_speed)

    def set_view_connections(self):
        self.window.btnBack.clicked.connect(lambda: self.w_player.go_back(self.m_player.ms_back))
        self.window.play_pause_action.triggered.connect(self.play_pause)
        self.window.btnForward.clicked.connect(lambda: self.w_player.go_forward(self.m_player.ms_forward))
        self.window.speed_slider.valueChanged.connect(self.changeSpeedVideo)


if __name__ == '__main__':
    c = Controller()