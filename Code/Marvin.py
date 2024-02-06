import time, os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import serial

com = serial.Serial(port='COM5',
                    baudrate =9600,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    timeout=1)

#Speech_to_text
def listen(recognizer, audio):
    try:
        global text
        text=''
        text = recognizer.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        print('Recognition Failure') # fail speech recognition
    except sr.RequestError as e:
        print('Request Error : {0}'.format(e)) # API Key error, Network Error

#LLM
def answer(input_text):
    global answer_text
    answer_text=''
    if 'bathroom' in input_text:
        answer_text='Go straight and turn right'
        return True
    elif 'professor' in input_text:
        answer_text= 'He is on the 5th floor in the FTC building'
        return True
    else:
        answer_text="Sorry, I could not understand what you were talking about."
        return False

    
    #stop_listening(wait_for_stop=False)

#Text_to_Speech
def speak(text):
    file_name = 'voice.mp3'
    print('[Marvin]:'+text)
    tts=gTTS(text=text, lang='en-US')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)


r = sr.Recognizer()
m = sr.Microphone(device_index=1)
stop_listening=r.listen_in_background(m,listen)
IDLE = 0
ACTIVATED = 1 
ROTATING = 2
LISTENING =3 
THINKING = 4
RESPONDING = 5
FAIL = 6
ack=1
currentState = IDLE
text=''

thinkingCount = 0
MarvinCount=0

while True:
    
    if com.in_waiting != 0:
        data=com.readline()
        ack=int(data.decode())
        print("ack : ", ack, "current : ", currentState)
        
        ### 0 IDLE ###
        if (currentState == IDLE):
            print("IDLE")
            print("############", text)
            if text != '':
                if text != 'Marvin':
                    speak("My name is Marvin. If you have questions, call my name")
                    time.sleep(3)
                    text = ''
                elif text=='Marvin':
                    currentState = ACTIVATED
                    com.write(str(currentState).encode())
                    MarvinCount = 0
            # if(MarvinCount == 20):
            #     speak("My name is Marvin. Do you need any help?")
            #     time.sleep(3)
            #     currentState = ACTIVATED
            #     com.write(str(currentState).encode())
            #     MarvinCount=0
            # MarvinCount += 1
        ### 1 ACTIVATED ###
        elif (currentState == ACTIVATED):
            print("ACTIVATED")
            MarvinCount = 0
            currentState = ROTATING
            com.write(str(currentState).encode())
        ### 2 ROTATING ###
        elif (currentState == ROTATING):
            print("ROTATING")
            speak ('Hello, I am Marvin. Do you need any help?')
            time.sleep(3)
            text=''
            currentState = LISTENING
            com.write(str(currentState).encode())
        ### 3 LISTENING ###
        elif (currentState == LISTENING):
            print("LISTENING")
            if text !='':
                print('[Group4_LISTENING]:'+text)
                currentState = THINKING
                com.write(str(currentState).encode())
                thinkingCount = 0
            if(thinkingCount == 20):
                speak("Sorry. I could not hear anything.")
                time.sleep(3)
            elif(thinkingCount == 40):
                speak("Sorry, Try again")
                time.sleep(3)
                currentState =  IDLE
                com.write(str(currentState).encode())
            thinkingCount += 1
            
        ### 4 THINKING ###
        elif (currentState == THINKING):
            print("THINKING")
            thinkingCount = 0
            result = answer(text)
            currentState = RESPONDING
            com.write(str(currentState).encode())
        ### 5 RESPONDING ###
        elif (currentState == RESPONDING):
            print("RESPONDING")
            if result == True:
                speak(answer_text)
                time.sleep(3)
                text=''
                currentState =  IDLE
                com.write(str(currentState).encode())
            elif result == False:
                speak(answer_text)
                time.sleep(3)
                text=''
                currentState =  FAIL
                com.write(str(currentState).encode())
                time.sleep(2)
                currentState =IDLE              
        else:
            print('currentState Error')
        print("send state : ", currentState)
        # com.write(str(currentState).encode())