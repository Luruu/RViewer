'''
    controller
'''

from view import View
from model import Model
import sys

class Controller():
    def __init__(self):
        
        # source_path is for testing only
        source_path = "test/test_sub.mkv"
        sys.argv += [source_path]

        view = View(sys.argv[1])
        model = Model(back=10,forward=30)

        self.window = view.window
        self.w_player = view.player

        self.m_player = model.player

        self.set_view_connections()
        
        self.play_pause()
        self.window.timer.start()
        self.w_player.parse_media()

        self.window.show() 
        self.m_player.video_info["duration"] = self.w_player.get_duration()
        self.window.loadbar.setMaximum(self.m_player.video_info["duration"])
        self.m_player.video_info["rate"] = self.w_player.get_rate()

        # print(type(self.w_player.vlc_player.get_full_title_descriptions()))
        print("[test] n_subtitles:", self.w_player.get_sub_count())
        print("[test] get_subtitles:", self.w_player.get_sub())
        print("[test] get_sub_descriptions:", self.w_player.get_sub_descriptions())
        
        
        sys.exit(self.window.app.exec())
    

    def play(self):
        self.w_player.play()
        self.w_player.is_paused = True
        self.window.play_pause_action.setIcon(self.window.icon_pause)
        self.window.timer.start()
        
    def pause(self):
        self.w_player.pause()
        self.w_player.is_paused = False
        self.window.play_pause_action.setIcon(self.window.icon_play)
        self.window.timer.stop()

    def play_pause(self):
        self.pause() if self.w_player.is_playing() else self.play()

    def changeSpeedVideo(self):
        # for example: value on trackbar for 1.0x is 5, so 5/5 = 1. For 2.0x is 10, so 10/5 = 2 and so on.
        new_speed = self.window.speed_slider.value() / 5
        self.window.label_speed.setText(" " + str(new_speed) + "x")
        self.w_player.set_rate(new_speed)

    def update_gui(self):
        # print(int(self.w_player.get_time()))
        time = self.w_player.get_time()
        self.window.loadbar.setValue(int(time))
        self.window.labelposition.setText(self.m_player.convert_ms_to_hmmss(time))
        self.window.labelduration.setText(self.m_player.convert_ms_to_hmmss(self.m_player.video_info["duration"] - time))
        if not self.w_player.is_playing(): # if is paused or stopped
            self.window.timer.stop()
            self.window.play_pause_action.setIcon(self.window.icon_pause)
            if not self.w_player.is_paused: #if is stopped
                self.w_player.stop()


    def slider_clicked(self):
        ''' This slot is only just used to handle mouse clicks.'''
        if self.window.loadbar.mouse_pressed:
            self.window.loadbar.mouse_pressed = False
           
            time = self.window.loadbar.value()
            self.w_player.set_time(time)
            self.window.labelposition.setText(self.m_player.convert_ms_to_hmmss(time))
            self.window.labelduration.setText(self.m_player.convert_ms_to_hmmss(self.m_player.video_info["duration"]  - time))
            
    def set_view_connections(self):
        self.window.btnBack.clicked.connect(lambda: self.w_player.go_back(self.m_player.ms_back))
        self.window.play_pause_action.triggered.connect(self.play_pause)
        self.window.btnForward.clicked.connect(lambda: self.w_player.go_forward(self.m_player.ms_forward))
        self.window.speed_slider.valueChanged.connect(self.changeSpeedVideo)
        self.window.timer.timeout.connect(self.update_gui)

        self.window.loadbar.sliderMoved.connect(lambda: self.w_player.set_time(self.window.loadbar.value()))
        self.window.loadbar.sliderPressed.connect(lambda: self.pause)
        self.window.loadbar.sliderReleased.connect(lambda: self.play)
        self.window.loadbar.valueChanged.connect(self.slider_clicked)
      

        
if __name__ == '__main__':
    c = Controller()