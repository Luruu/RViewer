'''
    view
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import vlc
import sys

    
class PlayerView(QThread):

    def __init__(self, controller):
        QThread.__init__(self)
        self.vlc_istance = None
        self.vlc_player = None
        self.media = None
        self.controller = controller

    def run(self):
        self.video_path = sys.argv[1]
        self.vlc_istance = vlc.Instance("--verbose -1")
        self.vlc_player = self.vlc_istance.media_player_new()
        self.media = self.vlc_istance.media_new(sys.argv[1])
        self.vlc_player.set_media(self.media)       
        self.is_paused = False
        self.controller.sem_player.release(1)
        
    
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
    def __init__(self, controller):
        super(PreferencesView, self).__init__()
        self.controller = controller
        self.player_preferences = self.controller.m_player.player_preferences
        self.nameprogram = self.controller.program_name
        self.setWindowTitle(self.nameprogram + " preferences")

        
        self.setFixedSize(240, 480)
        self.set_widgets()
        self.add_widgets()
        self.track_bar_conversion = 5
       

    def showEvent(self, event):
        self.spinbox1.setValue(int(self.player_preferences["back_value"]))
        self.text1.setText(self.player_preferences["back_shortkey"])
        self.spinbox2.setValue(int(self.player_preferences["forward_value"]))
        self.text2.setText(self.player_preferences["forward_shortkey"])
        self.text3.setText(self.player_preferences["playpause_shortkey"])
        self.spinbox3.setValue(float(self.player_preferences["track_value"] / self.track_bar_conversion))
        
        self.checkbox1.setChecked(self.player_preferences["loop_video"])
        self.checkbox2.setChecked(self.player_preferences["pick_up_where_you_left_off"])
        self.checkbox3.setChecked(self.player_preferences["track_video"])
        self.checkbox4.setChecked(self.player_preferences["show_subtitle_if_available"])
        

    def unsaved_changes(self):
        back_changed = self.player_preferences["back_value"] != self.spinbox1.value()
        forward_changed = self.player_preferences["forward_value"] != self.spinbox2.value()
        track_changed = self.player_preferences["track_value"] != int(self.spinbox3.value() * self.track_bar_conversion)
        loop_changed = self.player_preferences["loop_video"] != self.checkbox1.isChecked()
        pick_changed = self.player_preferences["pick_up_where_you_left_off"] != self.checkbox2.isChecked()
        trackvideo_changed = self.player_preferences["track_video"] != self.checkbox3.isChecked()
        show_changed = self.player_preferences["show_subtitle_if_available"] != self.checkbox4.isChecked()
       
        back_short_changed = self.player_preferences["back_shortkey"] != self.text1.text()
        forward_short_changed = self.player_preferences["forward_shortkey"] != self.text2.text()
        playpause_short_changed = self.player_preferences["playpause_shortkey"] != self.text3.text()
        

        return back_changed or forward_changed or track_changed or loop_changed or pick_changed or trackvideo_changed or show_changed or back_short_changed or playpause_short_changed or forward_short_changed
    
    def changes_applied(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(self.nameprogram + " changes applied.")
        dlg.setText("Changes applied. please reopen the video player.")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.setIcon(QMessageBox.Information)
        button = dlg.exec_()
    
    def accept(self):
        if self.unsaved_changes():
            track_bar_conversion = 5
            self.controller.m_player.save_player_preferences(back=self.spinbox1.value(),forward=self.spinbox2.value(),track_pos=int(self.spinbox3.value() * track_bar_conversion),
                                                         loop=self.checkbox1.isChecked(),pick=self.checkbox2.isChecked(), save=self.checkbox3.isChecked(),show=self.checkbox4.isChecked(), 
                                                         back_short=self.text1.text(), forwd_short=self.text2.text(), plpau_short =self.text3.text())
            self.changes_applied()
        super().accept()
        
    
    def reject(self):
        if self.unsaved_changes():
            dlg = QMessageBox(self)
            dlg.setWindowTitle(self.nameprogram + " unsaved changes")
            dlg.setText("There are values that have not been saved. Do you want to save the changes?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec_()
            if button == QMessageBox.Yes:
                self.accept()
        
        super().reject()
        

    def restore(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(self.nameprogram + " restore default values")
        dlg.setText("Are you sure to restore default values?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Question)
        button = dlg.exec_()
        if button == QMessageBox.Yes:
            self.controller.m_player.player_preferences = self.controller.m_player.default_player_preferences 
            self.close()

    def set_widgets(self):
        self.layoutt = QFormLayout()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
    
        self.restorebutton = QPushButton()
        self.restorebutton.setText("Restore")
        self.restorebutton.setStyleSheet('QPushButton {background-color: red}')
        self.restorebutton.clicked.connect(self.restore)

        self.spinbox1 = QSpinBox()
        self.spinbox1.setMinimum(1)
        
        self.spinbox2 = QSpinBox()
        self.spinbox2.setMinimum(1)
        
        self.spinbox3 = QDoubleSpinBox()
        self.spinbox3.setMaximum(2)
        self.spinbox3.setMinimum(0.2)
        self.spinbox3.setSingleStep(0.2)
        self.spinbox3.setDecimals(1)
        
        self.spinbox3.lineEdit().setReadOnly(True) # edit disabled but arrows enabled

        self.checkbox1 = QCheckBox("loop video")
        self.checkbox2 = QCheckBox("pick up where you left off")
        self.checkbox3 = QCheckBox("use video speed instead player speed")
        self.checkbox4 = QCheckBox("show subtitle (if available) at startup")

        self.text1 = QLineEdit()
        self.text2 = QLineEdit()
        self.text3 = QLineEdit()

        self.labelspeed1 = QLabel("The player speed value is used for")
        self.labelspeed2 = QLabel("videos that you have never played.\n")
        self.labelspeed1.setStyleSheet("QLabel {color: #4c4c4c;}")
        self.labelspeed2.setStyleSheet("QLabel {color: #4c4c4c;}")


    def add_widgets(self):
        self.layoutt.setSpacing(10)
        self.layoutt.addRow(self.restorebutton)
        self.layoutt.addRow(QLabel("back value:"), self.spinbox1)
        self.layoutt.addRow(QLabel("back short key:") , self.text1)
        self.layoutt.addRow(QLabel("forward value:"), self.spinbox2)
        self.layoutt.addRow(QLabel("forward short key:") , self.text2)
        self.layoutt.addRow(QLabel("play/pause short key:") , self.text3)
        self.layoutt.addRow(QLabel("player speed value:"),self.spinbox3)
        self.layoutt.addRow(self.labelspeed1) 
        self.layoutt.addRow(self.labelspeed2)
        self.layoutt.addRow(self.checkbox1)
        self.layoutt.addRow(self.checkbox2)
        self.layoutt.addRow(self.checkbox3)
        self.layoutt.addRow(self.checkbox4)
        self.layoutt.addRow(self.button_box)
        
        self.setLayout(self.layoutt)




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
        self.app.setApplicationName(name_program)
        print(self.app.style())
        self.app.setApplicationVersion("1.0")
        # ------ TO-DO: CHECK HERE IF ARGV[1] IS A PATH OF A VIDEO
        
        self.app.setStyle('Fusion')
        super().__init__()
        self.preference_window = PreferencesView(controller=self.controller)
        available_geometry = self.screen().availableGeometry()

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
       
        
        
        self.label_speed = QLabel(self)
        
        self.label_speed.setAlignment(Qt.AlignCenter)
    
        self.labelduration = QLabel(self)
        self.labelduration.setText("00:00:00")
        self.labelduration.setAlignment(Qt.AlignCenter)


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
        self.btnSubtitle.setText("show subtitles")
       
        

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
    

    