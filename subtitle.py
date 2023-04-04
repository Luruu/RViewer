''' 
    Model
'''
import time
import os.path
import datetime
import sys
import whisper 
import torch
class Whisper():
    
    def __init__(self, name_video , path_video, lang_sub, model_selected):
            self.name_video = name_video
            self.path_video = path_video

            self.model = None

            self.lang_sub = lang_sub
            self.model_selected = model_selected
            
            
    def run(self):
        

        ''' imports are here because too heavy to import at startup'''
        print("starting Whisper..") 
        
        
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        print("{}: Loading Whisper {} Model on\n '{}' [torch.cuda {}]".format(time.strftime("%H:%M:%S", time.localtime()), self.model_selected.upper(), "GPU" if DEVICE == "cuda" else "CPU", "available" if DEVICE == "cuda" else "NOT available")) 
        

        if self.model is None:
            self.model = whisper.load_model(self.model_selected, device=DEVICE)
        
        print("{}: Creating Subtitles...".format(time.strftime("%H:%M:%S", time.localtime())))
    
        result = self.model.transcribe(self.path_video, verbose=False, without_timestamps=False, language=self.lang_sub, fp16 = False)

        print("{}: Subtitles created!".format(time.strftime("%H:%M:%S", time.localtime()))) 

        srt_file_name = os.path.join('srt', "{}.srt".format(self.name_video))
       
        self.create_srt(srt_file_name, result)
        print("{}: srt file Subtitles created!".format(time.strftime("%H:%M:%S", time.localtime()))) 
        

    def create_srt(self,srt_file_name, result):
        self.str_out = ""
        for key in result["segments"]:
            self.str_out += "{}\n{} --> {}\n{}\n\n".format(key["id"]+1, self.convert_ss_to_hmmss(key["start"]),self.convert_ss_to_hmmss(key["end"]),key["text"])
        
        with open(srt_file_name, 'w', encoding="utf-8") as f:
            f.write(self.str_out)

    def convert_ss_to_hmmss(self, ss):
        return str(datetime.timedelta(seconds=ss))


if __name__ == '__main__':
    if len(sys.argv) > 0:
        Whisper(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]).run()
    else:
        print("error: no arguments")
