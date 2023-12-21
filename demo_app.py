from elevenlabs import generate, save, stream
from playsound import playsound
import speech_recognition as sr
from utils.core import chat
from dotenv import load_dotenv
from os import environ
from pygame import mixer
from playsound import playsound

load_dotenv()

mixer.init()
mixer.music.load('./data/audio/wait.mp3')


def tts(text: str, voice_id: str = "knrPHWnBmmDHMoiMeP3l", tryCount=1): # santa
    try:
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_multilingual_v1",
            api_key=environ["ELEVANLABS_API_KEY"],
            stream=True
        )
        # audioFilePath = "./data/audio/audio.mp3"
        stream(audio)
    except Exception as e:
        print(e)
        # tts(text=text, tryCount=tryCount+1)
    # save(audio, filename=audioFilePath)
    # playsound(audioFilePath)


r = sr.Recognizer()
r.pause_threshold = 0.7  # pause threshold
#mixer.music.play()


while True:
    with sr.Microphone(device_index=1) as source:
        # mixer.music.stop()
        print("Listening for Hey 🎙️")
        # audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        #mixer.music.play()
        transcript = r.recognize_whisper(audio, language="english")
        print(f"😃: {transcript}")
        if "hey" in transcript.lower():
            #while True:
                # playsound("./data/audio/jingle_bells.mp3")
                #mixer.music.stop()
                #rint("Listening 🎙️")
                #audio = r.listen(source)
                #transcript = r.recognize_whisper(audio, language="english")
                if "bye" in transcript.lower(): 
                    playsound("./data/audio/bye.mp3")
                    break
                if transcript != "":
                    mixer.music.stop()
                    print("Thinking 🤔")
                    mixer.music.play()
                    response = chat(question=transcript)
                    # print("Speaking 🔊")
                    # print(f"😺: {response}")
                    mixer.music.stop()
                    tts(text=response)
      
      
                
