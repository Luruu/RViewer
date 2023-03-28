'''
    view
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import vlc
import sys

    
class PlayerView():
    def __init__(self, video_path):
        self.video_path = video_path
        self.vlc_istance = vlc.Instance("--verbose -1")
        self.vlc_player = self.vlc_istance.media_player_new()
        self.media = self.vlc_istance.media_new(video_path)
        self.vlc_player.set_media(self.media)       
        self.is_paused = False
    
    
    def get_media(self):
        return self.media

    def get_video_property(self, e_meta):
        return self.media.get_meta(e_meta)

    
    def get_istance_vlc_player(self):
        return self.vlc_player
        
    def set_subtitle(self, subtitle_path):
        self.vlc_player.video_set_subtitle_file(subtitle_path)
    
    def play(self):
        return self.vlc_player.play()
    
    def pause(self):
        return self.vlc_player.pause()
    
    def stop(self):
        return self.vlc_player.stop()
    
    def is_playing(self):
        return self.vlc_player.is_playing()
    
    def parse_media(self):
        return self.media.parse()
    
    def go_back(self, ms):
        self.set_time(max(self.get_time() - ms, 0))

    def go_forward(self, ms):
        new_t = self.get_time() + ms
        if new_t < self.get_duration():
            self.set_time(new_t)

    def get_state(self):
        return self.vlc_player.get_state()
    
    def get_duration(self):
        return self.vlc_player.get_length()
    
    def get_time(self):
        return self.vlc_player.get_time()
    
    def set_time(self, i_time):
        return self.vlc_player.set_time(i_time)
    
    def get_position(self):
        return self.vlc_player.get_position()
    
    def set_position(self, f_pos):
        return self.vlc_player.set_position(f_pos)
    
    def get_rate(self):
        return self.vlc_player.get_rate()
    
    def set_rate(self, rate):
        return self.vlc_player.set_rate(rate)
    
    def get_state(self):
        return self.vlc_player.get_state()
    
    def get_sub_count(self):
        return self.vlc_player.video_get_spu_count()
    
    def get_sub(self):
        return self.vlc_player.video_get_spu()
    
    def get_sub_descriptions(self):
        return self.vlc_player.video_get_spu_description()
    
    def get_sub_delay(self):
        return self.vlc_player.video_get_spu_delay()
    
    def set_sub_delay(self, delay):
        return self.vlc_player.video_set_spu_delay(delay)
   
    def set_volume(self, volume):
        return self.vlc_player.audio_set_volume(volume)
    
    def get_volume(self):
        return self.vlc_player.audio_get_volume()


class PreferencesView(QDialog):
    def __init__(self,name_program):
        super(PreferencesView, self).__init__()
        available_geometry = self.screen().availableGeometry()
        self.resize(available_geometry.width() / 6,
                        available_geometry.height() / 3)
        
        self.setWindowTitle(name_program + " preferences")
        
        self.set_widgets()
        self.add_widgets()

    def accept(self):
        super.accept()


    def set_widgets(self):
        self.layoutt = QFormLayout()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.labelback = QLabel(self)
        self.labeltextEdit = QTextEdit()
        self.labeltextEdit2 = QTextEdit()
        self.labelback.setText("back value:")
        # self.labelback.setAlignment(Qt.AlignCenter)

        self.btnapply = QPushButton(self)
        self.btnapply.setText("Apply")
    
    def add_widgets(self):
        self.layoutt.addRow(QLabel("Line 1:"), QLineEdit())
        self.layoutt.addRow(QLabel("Line 2, long text:"), QComboBox())
        self.layoutt.addRow(QLabel("Line 3:"), QSpinBox())
        
        self.setLayout(self.layoutt)
        print("2")




class WindowView(QMainWindow):
    def __init__(self, name_program, controller, player_user_preferences):
        self.controller = controller # used in close_event()
        
        loadbar_css = "css/loadbar_style.css"
        sliderbar_css = "css/speed_slider.css"
        
        with open(loadbar_css, 'r') as f:
            self.loadbar_style = f.read()

        with open(sliderbar_css, 'r') as f:
            self.speedslider_style = f.read()
        
        if sys.platform == "win32": # for Windows
            sys.argv += ['-platform', 'windows:darkmode=1']
        
        self.app = QApplication(sys.argv)

        # ------ TO-DO: CHECK HERE IF ARGV[1] IS A PATH OF A VIDEO
        
        self.app.setStyle('Fusion')
        super().__init__()
        self.preference_window = PreferencesView(name_program)
        available_geometry = self.screen().availableGeometry()
        self.resize(available_geometry.width() / 3,
                        available_geometry.height() / 2.5)
        
        self.setWindowTitle(name_program)
        
        self.set_widgets(player_user_preferences)

        self.add_widgets()
        
    def show_preference_window(self):
        self.preference_window.show()

    def set_widgets(self, player_user_preferences):
        self.videoframe = QFrame()

        # set videoframe color
        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        self.setCentralWidget(self.videoframe)

        self.labelposition = QLabel(self)
        self.labelposition.setText("00:00:00")
        self.labelposition.setAlignment(Qt.AlignCenter)
        

        self.tool_bar = QToolBar()
        self.tool_bar2 = QToolBar()
        self.tool_bar3 = QToolBar()

        self.tool_bar.setMovable(False)

        # toolbar shown on second toolbar
        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar2)
        self.addToolBar(Qt.TopToolBarArea, self.tool_bar3)
        
        self.btnBack = QPushButton(self)
        self.btnBack.setText("-{}".format(player_user_preferences["back_value"]))
        self.btnBack.setShortcut('Ctrl+D')

        

        
        style = self.style()
        self.icon_play = QIcon.fromTheme("media-playback-start.png",
                             style.standardIcon(QStyle.SP_MediaPlay))
        self.icon_pause = QIcon.fromTheme("media-playback-pause.png",
                               style.standardIcon(QStyle.SP_MediaPause))
        

        self.btnForward = QPushButton(self)
        self.btnForward.setText("+{}".format(player_user_preferences["forward_value"]))   
        self.btnForward.setShortcut('Ctrl+F')  
        
        
        
        self.loadbar = SliderClicker()
        self.loadbar.setOrientation(Qt.Horizontal)
        self.loadbar.setMinimum(0)
        self.loadbar.setMaximum(1)
        self.loadbar.setSingleStep(1)
        self.loadbar.setStyleSheet(self.loadbar_style)  

        
        self.speed_slider = SliderClicker()
        self.speed_slider.setOrientation(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        available_width = self.screen().availableGeometry().width()
        self.speed_slider.setFixedWidth(available_width / 12)
        self.speed_slider.setValue(player_user_preferences["track_value"]) #default playback value of a video (5/5 = 1.0x)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(SliderClicker.TicksBelow)
        self.speed_slider.setToolTip("speed video")
        self.speed_slider.setStyleSheet(self.speedslider_style)  
       
        
        
        self.label_speed = QLabel(self)
        
        self.label_speed.setText(player_user_preferences["label_track_value"])
        self.label_speed.setAlignment(Qt.AlignCenter)
    
        self.labelduration = QLabel(self)
        self.labelduration.setText("00:00:00")
        self.labelduration.setAlignment(Qt.AlignCenter)

        
        self.timer = QTimer(self)
        self.timer.setInterval(500)


        self.spacer1 = QWidget()
        self.spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.spacer2 = QWidget()
        self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        '''
        self.spacer3 = QWidget()
        self.spacer3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer4 = QWidget()
        self.spacer4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer5 = QWidget()
        self.spacer5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer6 = QWidget()
        self.spacer6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spacer7 = QWidget()
        self.spacer7.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        '''
        self.btnpreferences = QPushButton(self)
        self.btnpreferences.setText("preferences")

        self.btnSubtitle = QPushButton(self)
        self.btnSubtitle.setText("show Subtitles")
       
        

    def add_widgets(self):
        

        self.tool_bar.addWidget(self.spacer1)
        self.tool_bar.addWidget(self.btnBack)
        self.play_pause_action = self.tool_bar.addAction(self.icon_play, "")
        self.tool_bar.addWidget(self.btnForward)
        self.tool_bar.addWidget(self.spacer2)


        self.tool_bar2.addWidget(self.labelposition)
        self.tool_bar2.addWidget(self.loadbar)
        self.tool_bar2.addWidget(self.labelduration)


        self.tool_bar3.addWidget(self.speed_slider)
        self.tool_bar3.addWidget(self.label_speed) 
        self.tool_bar3.addWidget(self.btnSubtitle)
        self.tool_bar3.addWidget(self.btnpreferences)
        
        
    
    def set_loadbar2orientation(self):
        if self.loadbar.orientation() == Qt.Horizontal:
            self.loadbar.setOrientation(Qt.Vertical)
        else:
            self.loadbar.setOrientation(Qt.Horizontal)
    def closeEvent(self, event):
        print(self.speed_slider.value(),self.loadbar.value())
        self.controller.close_program(event, track_pos=self.speed_slider.value(), load_pos=self.loadbar.value())


class SliderClicker(QSlider):

    ''' ----------------  WHY SLIDERCICKER CLASS IS USED?
        this class is useful for handling the "mousepressEvent" event which is not normally supported by QSlider.
    '''
    def __init__(self):
        super().__init__()
        self.mouse_pressed = False # this boolean variable can be used for checking if mouse is pressed.
        

    def mousePressEvent(self, event):
        super(SliderClicker, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)
            
            

    def pixelPosToRangeValue(self, pos):
        opt = QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

        if self.orientation() == Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)
    

    