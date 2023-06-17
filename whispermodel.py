''' 
    Model
'''
import time
import os.path
import datetime
import sys
import whisperx
import torch
class Whisper():
    
    def __init__(self, program_path, name_video, path_video, lang_sub, model_selected):
            self.name_video = name_video
            self.path_video = path_video
            self.program_path = program_path

            self.model = None
            self.lang_sub = lang_sub
            self.model_selected = model_selected
            self.batch_size = 4 # reduce if low on GPU mem
            self.compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)
            
            
    def run(self):
        
        print("starting WhisperX..") 
        
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        print("{}: Loading Whisper {} Model on\n '{}' [torch.cuda {}]".format(time.strftime("%H:%M:%S", time.localtime()), self.model_selected.upper(), "GPU" if DEVICE == "cuda" else "CPU", "available" if DEVICE == "cuda" else "NOT available")) 
        

        if self.model is None:
            self.model = whisperx.load_model(self.model_selected, language=self.lang_sub, device=DEVICE, compute_type=self.compute_type)
        
        audio = whisperx.load_audio(self.path_video)

        print("{}: WhisperX 1. -> TRASCRIPTION started...".format(time.strftime("%H:%M:%S", time.localtime())))

        # 1. Transcribe with original whisper (batched)

        result = self.model.transcribe(audio, language=self.lang_sub, batch_size=self.batch_size)

        print("{}: TRANSCRIBE OPERATION COMPLETED!".format(time.strftime("%H:%M:%S", time.localtime())))

        print("{}: WhisperX 2. -> ALIGNMENT started...".format(time.strftime("%H:%M:%S", time.localtime())))

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code="en", device=DEVICE)
       
        result = whisperx.align(result["segments"], model_a, metadata, audio, DEVICE, return_char_alignments=False)

        print("{}: ALIGNMENT OPERATION COMPLETED!".format(time.strftime("%H:%M:%S", time.localtime())))

        srt_file_name = os.path.join(self.program_path,'srt', "{}.srt".format(self.name_video))
        
        self.create_srt(srt_file_name, result)
        print("{}: srt file Subtitles created correctly!".format(time.strftime("%H:%M:%S", time.localtime()))) 
       

    def create_srt(self,srt_file_name, result):
        self.str_out = ""
        i=0
        for key in result["segments"]:
                i += 1
                self.str_out += "{}\n{} --> {}\n{}\n\n".format(str(i), self.format_td(key["start"]), self.format_td(key["end"]), key["text"])
        
        with open(srt_file_name, 'w', encoding="utf-8") as f:
            f.write(self.str_out)

    def format_td(self, seconds, digits=3):
        isec, fsec = divmod(round(seconds*10**digits), 10**digits)
        return ("{}.{:0%d.0f}" % digits).format(datetime.timedelta(seconds=isec), fsec)


if __name__ == '__main__':
    if len(sys.argv) > 0:
        Whisper(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]).run()
    else:
        print("error: no arguments")
