import speech_recognition as sr
r=sr.Recognizer()
with sr.Microphone() as source:
    print('listening')
    audio=r.listen(source)

try:
    text=r.recognize_google(audio,language='en-US')
    print(text)
except sr.UnknownValueError:
    print('Recognition Failure') # fail speech recognition
except sr.RequestError as e:
    print('Request Error : {0}'.format(e)) # API Key error, Network Error