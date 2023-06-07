'''
    view
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import sys
import os

from views import PreferencesView, WhisperView




class MainView(QMainWindow):
    def __init__(self, name_program, path_program, controller, player_user_preferences):
        
        self.controller = controller # used in close_event()

        dir_css_name = "styles"
        
        loadbar_css = os.path.join(path_program, dir_css_name, "loadbar_style.css") 
       
        sliderbar_css = os.path.join(path_program, dir_css_name, "speed_slider.css")

        print(loadbar_css)
        
        with open(loadbar_css, 'r') as f:
            self.loadbar_style = f.read()

        with open(sliderbar_css, 'r') as f:
            self.speedslider_style = f.read()

        #if user platform is windows and he want special dark mode..
        if sys.platform == "win32" and player_user_preferences["windows_dark_mode"]: # for Windows
            sys.argv += ['-platform', 'windows:darkmode=2']
        
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(name_program)
        self.app.setApplicationVersion("1.0")
        path_icon = os.path.join(path_program, 'img', "icon.png")
        self.app.setWindowIcon(QIcon(path_icon))
        
        self.app.setStyle('Fusion')
        super().__init__()
        self.preference_window = PreferencesView(controller=self.controller)
        self.whisper_window = WhisperView(controller=self.controller)
        available_geometry = self.screen().availableGeometry()

        # if is the first time that user open RViewer..
        if player_user_preferences["x"] == 0:
            self.resize(available_geometry.width() / 3,
                        available_geometry.height() / 2.5)
        else:
            self.setGeometry(player_user_preferences["x"], player_user_preferences["y"], player_user_preferences["dim"], player_user_preferences["hei"])
            
        
        self.setWindowTitle(name_program)
        
        self.set_widgets(player_user_preferences)

        self.add_widgets()
        
    def show_preference_window(self):
        self.preference_window.show()
    
    def show_whisper_window(self):
        self.whisper_window.show()

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
        self.tool_bar3.setAllowedAreas(Qt.BottomToolBarArea | Qt.TopToolBarArea)
        
        self.btnBack = QPushButton(self)
        self.btnBack.setStyleSheet('QPushButton {background-color: silver; color: black;}')
        self.btnBack.setText("-{}".format(player_user_preferences["back_value"]))
        self.btnBack.setShortcut(player_user_preferences["back_shortkey"])

        
        self.btnPlayPause = QPushButton(self)
        self.btnPlayPause.setStyleSheet('QPushButton {background-color: green; color: white;}')
        self.btnPlayPause.setFixedSize(105,30)  
        self.btnPlayPause.setText("||")   
        self.btnPlayPause.setShortcut(player_user_preferences["playpause_shortkey"])  
        
        

        self.btnForward = QPushButton(self)
        self.btnForward.setStyleSheet('QPushButton {background-color: silver; color: black;}')
        self.btnForward.setText("+{}".format(player_user_preferences["forward_value"]))   
        self.btnForward.setShortcut(player_user_preferences["forward_shortkey"])  
        
        
        
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
       
        self.volume_slider = SliderClicker()
        self.volume_slider.setOrientation(Qt.Vertical)
        self.volume_slider.setMinimum(1)
        self.volume_slider.setMaximum(125)
       
        available_width = self.screen().availableGeometry().width()
        self.volume_slider.setFixedHeight(22)
        self.volume_slider.setValue(100)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(SliderClicker.TicksLeft)
        
                                         
                                         
        self.label_speed = QLabel(self)
        
        self.label_speed.setAlignment(Qt.AlignCenter)
    
        self.labelduration = QLabel(self)
        self.labelduration.setText("00:00:00")
        self.labelduration.setAlignment(Qt.AlignCenter)


        self.spacer1 = QWidget()
        self.spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.spacer2 = QWidget()
        self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        
        self.spacer3 = QWidget()
        self.spacer3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.spacer4 = QWidget()
        self.spacer4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
     

        self.btnpreferences = QPushButton(self)
        self.btnpreferences.setText("preferences")

        self.btnSubtitle = QPushButton(self)
        self.btnSubtitle.setText("add subtitles")
       
        

    def add_widgets(self):
        

        self.tool_bar.addWidget(self.spacer1)
        self.tool_bar.addWidget(self.btnBack)
        self.tool_bar.addWidget(self.btnPlayPause)
        self.tool_bar.addWidget(self.btnForward)
        self.tool_bar.addWidget(self.spacer2)
        

        self.tool_bar2.addWidget(self.labelposition)
        self.tool_bar2.addWidget(self.loadbar)
        self.tool_bar2.addWidget(self.labelduration)


        self.tool_bar3.addWidget(self.speed_slider)
        self.tool_bar3.addWidget(self.label_speed) 
        self.tool_bar3.addWidget(self.btnSubtitle)
        self.tool_bar3.addWidget(self.btnpreferences)
        self.tool_bar3.addWidget(self.spacer3)
        self.tool_bar3.addWidget(QLabel("volume"))
        self.tool_bar3.addWidget(self.volume_slider)     

        
    
    def set_loadbar2orientation(self):
        if self.loadbar.orientation() == Qt.Horizontal:
            self.loadbar.setOrientation(Qt.Vertical)
        else:
            self.loadbar.setOrientation(Qt.Horizontal)
            
    def closeEvent(self, event):
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
    
