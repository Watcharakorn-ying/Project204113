
import speech_recognition as sr
from gtts import gTTS
import pyglet
import os

##class talktalk:
##    def __init__(self,recognize,file):
    ##recognize = 'ไม่เข้าใจในสิ่งที่คุณพูดค่ะ---...กรุณาพูดอีกครั้ง'
def talktalk(recognize,file):
    tts = gTTS(text=recognize, lang='th')
    tts.save(file)

    music = pyglet.resource.media(file)
    music.play()

##    self.File = file
    return
        
##os.system(helloFile)
    
if __name__ == '__main__':
##    r = sr.Recognizer()
##    m = sr.Microphone()
##
##    ##with m as source: 
##    with m as source:
##        r.adjust_for_ambient_noise(source)
##        audio = r.listen(source)
##        try:
##            recognize = r.recognize_google(audio,language = "th-TH")
##            print('you said :' + recognize)
##        except:
##            recognize = 'ไม่เข้าใจ กรุณาพูดอีกครั้งค่ะ'
##            print('not')
####    helloFile = talktalk('นำตัวเลข 63 ใส่เข้าไปแล้วค่ะ')
##    file = 'sound_simon/test.mp3'
    recognize = "ตัวเลขที่คุณคิดไว้...มีอยู่ในหน้านี้หรือไม่คะ"
    file = "06_talk_this_is_page.wav"
    helloFile = talktalk(recognize, file)
    music = pyglet.resource.media(helloFile.File)
    music.play()
    print('play')
