from gtts import gTTS

text='Hello, my name is marvin.'
file_name='sample.mp3'
tts_en=gTTS(text=text, lang='en-US')
tts_en.save(file_name)

#playing sound not making another mp3 file
from playsound import playsound
playsound(file_name)