'''
    controller
'''

from view import View
from model import Model
import sys
import vlc

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

        # saving video informations
        for key, value in vlc.Meta._enum_names_.items():
            self.m_player.video_info[value] = self.w_player.get_video_property(vlc.Meta(key))
        self.m_player.video_info["Subs"] = { "Count": self.w_player.get_sub_count(),
                                            "available" : self.w_player.get_sub(),
                                            "descriptions": self.w_player.get_sub_descriptions()}
        self.m_player.video_info["Rate"] = self.w_player.get_rate()
        self.m_player.video_info["Duration"] = self.w_player.get_duration()
        self.m_player.video_info["Duration_ss"] = self.w_player.get_duration() / 1000
        self.m_player.video_info["Duration_hh_mm_ss"] = self.m_player.convert_ms_to_hmmss(self.w_player.get_duration())
        
        print("video informations:", self.m_player.video_info)
        new_title = "RV - {} [{}]".format(self.m_player.video_info['Title'],self.m_player.video_info["Duration_hh_mm_ss"])
        self.window.setWindowTitle(new_title)
        self.window.loadbar.setMaximum(self.m_player.video_info["Duration"])
        
        
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
        time = self.w_player.get_time()
        self.window.loadbar.setValue(int(time))
        self.window.labelposition.setText(self.m_player.convert_ms_to_hmmss(time))
        self.window.labelduration.setText(self.m_player.convert_ms_to_hmmss(self.m_player.video_info["Duration"]- time))
                                                                            
    def timer_update_gui(self):
        self.update_gui()
        if not self.w_player.is_playing(): # if is paused or stopped
            self.window.timer.stop()
            self.window.play_pause_action.setIcon(self.window.icon_pause)
            if not self.w_player.is_paused: #if is stopped
                self.w_player.stop()


    def slider_clicked(self):
        ''' This slot is only just used to handle mouse clicks.'''
        if self.window.loadbar.mouse_pressed:
            self.window.loadbar.mouse_pressed = False
            self.w_player.set_time(self.window.loadbar.value())
            self.update_gui()
            
    def goback_and_update_gui(self):
        self.w_player.go_back(self.m_player.ms_back)
        self.update_gui()

    def goforward_and_update_gui(self):
        self.w_player.go_forward(self.m_player.ms_forward)
        self.update_gui()
    

    def set_view_connections(self):
        self.window.btnBack.clicked.connect(self.goback_and_update_gui)
        self.window.play_pause_action.triggered.connect(self.play_pause)
        self.window.btnForward.clicked.connect(self.goforward_and_update_gui)
        self.window.speed_slider.valueChanged.connect(self.changeSpeedVideo)
        self.window.timer.timeout.connect(self.timer_update_gui)

        self.window.loadbar.sliderMoved.connect(lambda: self.w_player.set_time(self.window.loadbar.value()))
        self.window.loadbar.sliderPressed.connect(lambda: self.pause)
        self.window.loadbar.sliderReleased.connect(lambda: self.play)
        self.window.loadbar.valueChanged.connect(self.slider_clicked)
      
        
if __name__ == '__main__':
    c = Controller()