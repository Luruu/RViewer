'''
    view
'''

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import vlc
import sys
import shutil
import os
    
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
    
    
    def play(self):
        return self.vlc_player.play()
    
    def pause(self):
        return self.vlc_player.pause()
    
    def stop(self):
        return self.vlc_player.stop()
    
    def is_playing(self):
        return self.vlc_player.is_playing()
    
    def get_state(self):
        return self.vlc_player.get_state()
    
    
    def parse_media(self):
        return self.media.parse()
    
    
    def go_back(self, ms):
        self.set_time(max(self.get_time() - ms, 0))

    def go_forward(self, ms):
        new_t = self.get_time() + ms
        if new_t < self.get_duration():
            self.set_time(new_t)

    
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
    
    
    def get_sub_count(self):
        return self.vlc_player.video_get_spu_count()
    
    def get_sub(self):
        return self.vlc_player.video_get_spu()
    
    def set_sub(self, i_spu):
        return self.vlc_player.video_set_spu(i_spu)
    
    def get_sub_descriptions(self):
        return self.vlc_player.video_get_spu_description()
    
    def get_sub_delay(self):
        return self.vlc_player.video_get_spu_delay()
    
    def set_sub_delay(self, delay):
        return self.vlc_player.video_set_spu_delay(delay)
    
    def set_subtitle(self, subtitle_path):
        return self.vlc_player.video_set_subtitle_file(subtitle_path)
    

    def get_audio_count(self):
        return self.vlc_player.audio_get_track_count()
    
    def get_audio_description(self):
        return self.vlc_player.audio_get_track_description()
    
    def get_istance_vlc_player(self):
        return self.vlc_player
    
   
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

        
        self.setFixedSize(245, 480)
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
        self.checkbox5.setChecked(self.player_preferences["windows_dark_mode"])
        

    def unsaved_changes(self):
        changes_list = []
        changes_list.insert(0,self.player_preferences["back_value"] != self.spinbox1.value())
        changes_list.insert(1,self.player_preferences["forward_value"] != self.spinbox2.value())
        changes_list.insert(2,self.player_preferences["track_value"] != int(self.spinbox3.value() * self.track_bar_conversion))
        changes_list.insert(3,self.player_preferences["loop_video"] != self.checkbox1.isChecked())
        changes_list.insert(4,self.player_preferences["pick_up_where_you_left_off"] != self.checkbox2.isChecked())
        changes_list.insert(5,self.player_preferences["track_video"] != self.checkbox3.isChecked())
        changes_list.insert(6,self.player_preferences["show_subtitle_if_available"] != self.checkbox4.isChecked())
        changes_list.insert(7,self.player_preferences["windows_dark_mode"] != self.checkbox5.isChecked())
       
        changes_list.insert(8,self.player_preferences["back_shortkey"] != self.text1.text())
        changes_list.insert(9,self.player_preferences["forward_shortkey"] != self.text2.text())
        changes_list.insert(10,self.player_preferences["playpause_shortkey"] != self.text3.text())
        
        return True in changes_list

    
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
                                                         back_short=self.text1.text(), forwd_short=self.text2.text(), plpau_short=self.text3.text(), darkmodewin=self.checkbox5.isChecked())
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
        self.restorebutton.setText("restore")
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
        self.checkbox5 = QCheckBox("special Dark Mode (Windows OS only)")
        if sys.platform == "win32": # for Windows
            self.checkbox5.setEnabled(True)
        else:
            self.checkbox5.setEnabled(False)

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
        self.layoutt.addRow(self.checkbox5)
        self.layoutt.addRow(self.button_box)
        
        self.setLayout(self.layoutt)


class WhisperView(QDialog):
    def __init__(self, controller):
        super(WhisperView, self).__init__()
        self.controller = controller
        self.nameprogram = self.controller.program_name
        self.name_video = ""
        self.setWindowTitle(self.nameprogram + " subtitles")

        
        self.setFixedSize(255, 300)
        self.set_widgets()
        self.add_widgets()

    def closeEvent(self, event):
        self.setEnabled(True)
        self.setFixedSize(255, 300)
        self.progressbar.setVisible(False)
        self.textedit.setVisible(False)
        self.controller.window.setEnabled(True)

    def import_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Text files (*.aqt *.cvd *.dks *.jss *.sub *.ttxt *.mpl *.txt *.pjs *.psb *.rt *.smi *.ssf *.srt *.ssa *.svcd *.usf*.idx)")
        filenames = ""
		
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            new_name = os.path.join(sys.path[0], 'srt', "{}.srt".format(self.name_video)) 
            shutil.copyfile(filenames[0],new_name)
            
            res = self.controller.w_player.set_subtitle(new_name)
            if  res == 1:
                print("subtitles added correctly")
                self.controller.buttonsub_operation = 0
                self.controller.window.btnSubtitle.setText("hide subtitles")
            else:
                print("error {}: cannot add subtitles".format(res))
            

    def set_widgets(self):
        self.layoutt = QFormLayout()

        self.label1 = QLabel("CREATE SUBTITLES WITH WHISPER")
        self.label1.setAlignment(Qt.AlignCenter)
        # self.label1.setStyleSheet("QLabel{font-size: 11pt;}")
        
    
        self.importbutton = QPushButton()
        self.importbutton.setText("Import subtitles from existing file")
        self.importbutton.clicked.connect(self.import_file)

        
        
        # print(list(LANGUAGES.keys())[list(LANGUAGES.values()).index("sundanese")])

        self.models = ["tiny", "base", "small"]
        self.languages = { "en": "english", "zh": "chinese", "de": "german", "es": "spanish", "ru": "russian", "ko": "korean", "fr": "french", "ja": "japanese", "pt": "portuguese", "tr": "turkish", "pl": "polish", "ca": "catalan", "nl": "dutch", "ar": "arabic", "sv": "swedish", "it": "italian", "id": "indonesian", "hi": "hindi", "fi": "finnish", "vi": "vietnamese", "he": "hebrew", "uk": "ukrainian", "el": "greek", "ms": "malay", "cs": "czech", "ro": "romanian", "da": "danish", "hu": "hungarian", "ta": "tamil", "no": "norwegian", "th": "thai", "ur": "urdu", "hr": "croatian", "bg": "bulgarian", "lt": "lithuanian", "la": "latin", "mi": "maori", "ml": "malayalam", "cy": "welsh", "sk": "slovak", "te": "telugu", "fa": "persian", "lv": "latvian", "bn": "bengali", "sr": "serbian", "az": "azerbaijani", "sl": "slovenian", "kn": "kannada", "et": "estonian", "mk": "macedonian", "br": "breton", "eu": "basque", "is": "icelandic", "hy": "armenian", "ne": "nepali", "mn": "mongolian", "bs": "bosnian", "kk": "kazakh", "sq": "albanian", "sw": "swahili", "gl": "galician", "mr": "marathi", "pa": "punjabi", "si": "sinhala", "km": "khmer", "sn": "shona", "yo": "yoruba", "so": "somali", "af": "afrikaans", "oc": "occitan", "ka": "georgian", "be": "belarusian", "tg": "tajik", "sd": "sindhi", "gu": "gujarati", "am": "amharic", "yi": "yiddish", "lo": "lao", "uz": "uzbek", "fo": "faroese", "ht": "haitian creole", "ps": "pashto", "tk": "turkmen", "nn": "nynorsk", "mt": "maltese", "sa": "sanskrit", "lb": "luxembourgish", "my": "myanmar", "bo": "tibetan", "tl": "tagalog", "mg": "malagasy", "as": "assamese", "tt": "tatar", "haw": "hawaiian", "ln": "lingala", "ha": "hausa", "ba": "bashkir", "jw": "javanese", "su": "sundanese",} 
        

        self.combobox2 = QComboBox()
        self.combobox2.addItems(self.languages)

    
        self.combobox3 = QComboBox()
        self.combobox3.addItems(self.models)


        self.createbutton = QPushButton()
        self.createbutton.setText("create subtitles")
        

        self.textedit = QTextEdit()
        # self.textedit.setVisible(False)
        self.textedit.setReadOnly(True)
        self.textedit.setFixedHeight(80)

        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(6)
        self.progressbar.setVisible(False)
    def add_widgets(self):
        self.layoutt.setSpacing(10)
        self.layoutt.addRow(self.importbutton)
        self.layoutt.addRow(QLabel(""))
        self.layoutt.addRow(self.label1)
        self.layoutt.addRow(QLabel("select Subtitle Language:"), self.combobox2)
        self.layoutt.addRow(QLabel("select Whisper Model:"), self.combobox3)
        # self.layoutt.addRow(QLabel(""))
        self.layoutt.addRow(self.textedit)
        self.layoutt.addRow(self.progressbar) 
        self.layoutt.addRow(self.createbutton)
      
        self.setLayout(self.layoutt)