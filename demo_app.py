from elevenlabs import generate, save
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

ELEVANLABS_API_KEY = environ["ELEVANLABS_API_KEY"]

def tts(text: str, voice_id: str = "knrPHWnBmmDHMoiMeP3l"): # santa
    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v1",
        api_key=ELEVANLABS_API_KEY,
    )
    audioFilePath = "./data/audio/audio.mp3"

    save(audio, filename=audioFilePath)
    playsound(audioFilePath)


r = sr.Recognizer()
r.pause_threshold = 0.7  # pause threshold
mixer.music.play()

while True:
    with sr.Microphone(device_index=1) as source:
        # mixer.music.stop()
        print("Listening for Hey 🎙️")
        # audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        # mixer.music.play()
        transcript = r.recognize_whisper(audio, language="english")
        print(f"😃: {transcript}")
        if "hey" in transcript.lower():
            while True:
                mixer.music.stop()
                print("Listening 🎙️")
                audio = r.listen(source)
                transcript = r.recognize_whisper(audio, language="english")
                if "bye" in transcript.lower(): 
                    break
                if transcript != "":
                    mixer.music.stop()
                    print("Thinking 🤔")
                    response = chat(question=transcript)
                    print("Speaking 🔊")
                    print(f"😺: {response}")
                    tts(text=response)
        mixer.music.play()
                
