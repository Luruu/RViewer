'''
    view
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


import vlc
import sys

class View():
    def __init__(self, source_path):
        self.player = PlayerView(source_path)
        self.window = WindowView(self.player.get_istance_vlc_player())
    
    
class PlayerView():
    def __init__(self, video_path):
        self.video_path = video_path
        self.vlc_istance = vlc.Instance()
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
        new_pos = self.get_time() - ms
        self.set_time(new_pos if new_pos >=0 else 0)
        print("a",self.get_time())

    
    def go_forward(self, ms):
        # self.pause()
        new_pos = self.get_time() + ms 
        duration = self.get_duration()
        self.set_time(new_pos if new_pos < duration else duration)
        print("b", new_pos, duration)

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


class WindowView(QMainWindow):
    def __init__(self,player):
        f = open("CSS/loadbar_style.css", "r")
        self.loadbar_style = f.read()
        f.close()
        f = open("CSS/speed_slider.css", "r")
        self.speedslider_style = f.read() 

        if sys.platform == "win32": # for Windows
            sys.argv += ['-platform', 'windows:darkmode=1']
        
        self.app = QApplication(sys.argv)

        # ------ DA CONTROLLARE SE IL PARAMETRO ARGV[1] è UN VIDEO O MENO! (o se è stato passato)
        
        self.app.setStyle('Fusion')
        super().__init__()
        available_geometry = self.screen().availableGeometry()
        self.resize(available_geometry.width() / 4,
                        available_geometry.height() / 3.5)

        
        self.setWindowTitle("RV")
        
        self.set_widgets()

        self.add_widgets(player)
        

    def set_widgets(self):
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

        # toolbar shown on second toolbar
        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.tool_bar2)


        self.btnBack = QPushButton(self)
        self.btnBack.setText("-10")        
        self.btnBack.setShortcut('Ctrl+D')
        # self.btnBack.move(100,100)

        
        style = self.style()
        self.icon_play = QIcon.fromTheme("media-playback-start.png",
                             style.standardIcon(QStyle.SP_MediaPlay))
        self.icon_pause = QIcon.fromTheme("media-playback-pause.png",
                               style.standardIcon(QStyle.SP_MediaPause))
        

        self.btnForward = QPushButton(self)
        self.btnForward.setText("+30")          #text
        self.btnForward.setShortcut('Ctrl+F')  #shortcut key
        # self.btnForward.move(100,100)
        
        # self.tool_bar2.addSeparator()
        
        self.loadbar = SliderClicker(self)
        self.loadbar.setOrientation(Qt.Horizontal)
        self.loadbar.setMinimum(0)
        self.loadbar.setMaximum(1)
        self.loadbar.setSingleStep(1)
        self.loadbar.setStyleSheet(self.loadbar_style)  

        
        self.speed_slider = QSlider()
        self.speed_slider.setOrientation(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(10)
        available_width = self.screen().availableGeometry().width()
        self.speed_slider.setFixedWidth(available_width / 10)
        self.speed_slider.setValue(5) #default playback value of a video (5/5 = 1.0x)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setToolTip("speed video")
        self.speed_slider.setStyleSheet(self.speedslider_style)  
        
        
        self.label_speed = QLabel(self)
        self.label_speed.setText(" 1.0x")
        self.label_speed.setAlignment(Qt.AlignCenter)
        

        self.left_spacer1 = QWidget()
        self.left_spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.labelduration = QLabel(self)
        self.labelduration.setText("00:00:00")
        self.labelduration.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        
        self.timer = QTimer(self)
        self.timer.setInterval(500)

        self.right_spacer1 = QWidget()
        self.right_spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.right_spacer2 = QWidget()
        self.right_spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_todo = QLabel(self)
        self.label_todo.setText("TO-DO")
        self.label_todo.setAlignment(Qt.AlignCenter)


    def add_widgets(self, player):
        self.tool_bar2.addWidget(self.labelposition)
        self.tool_bar2.addWidget(self.loadbar)
        self.tool_bar2.addWidget(self.labelduration)

        
        # self.tool_bar.addWidget(self.left_spacer1)
        self.tool_bar.addWidget(self.right_spacer1)

        self.tool_bar.addWidget(self.btnBack)

        self.play_pause_action = self.tool_bar.addAction(self.icon_play, "Play/Pause")
        self.tool_bar.addWidget(self.btnForward)

        #self.tool_bar.addWidget(self.right_spacer1)
        self.tool_bar.addWidget(self.speed_slider)
        self.tool_bar.addWidget(self.label_speed)   
        self.tool_bar.addWidget(self.right_spacer2)
        
        self.tool_bar.addWidget(self.label_todo)
        
        self.anchorVLCtoWindow(player, self.videoframe.winId())
     

    def anchorVLCtoWindow(self, player, id):
        if sys.platform.startswith('linux'): # for Linux using the X Server
            player.set_xwindow(id)
        elif sys.platform == "win32": # for Windows
            player.set_hwnd(id)
        elif sys.platform == "darwin": # for MacOS
            player.set_nsobject(id)
        else:
            print("ERROR: this software does not work with", sys.platform)
            exit()


class SliderClicker(QSlider):

    ''' ----------------  WHY SLIDERCICKER CLASS IS USED?
        this class is useful for handling the "mousepressEvent" event 
        which is not normally supported by QSlider. To update the video player time, 
        the "valueChanged" signal is used taking into account the boolean variable "self.mouse_pressed".
    '''
    def __init__(self, window):
        super().__init__()
        self.mouse_pressed = False 
        self.window = window
        

    def mousePressEvent(self, event):
        super(SliderClicker, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)
            # Mouse_pressed will be turn false using a slot function into the controller!
            

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