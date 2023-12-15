from elevenlabs import generate, save
from playsound import playsound
import speech_recognition as sr
from utils.core import chat
from dotenv import load_dotenv
from os import environ

load_dotenv()

ELEVANLABS_API_KEY = environ["ELEVANLABS_API_KEY"]

# santa knrPHWnBmmDHMoiMeP3l
def tts(text: str, voice_id: str = "knrPHWnBmmDHMoiMeP3l"):
    audio = generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v1",
        api_key=ELEVANLABS_API_KEY,
    )
    audioFilePath = "./data/audio.mp3"

    save(audio, filename=audioFilePath)
    playsound(audioFilePath)


r = sr.Recognizer()
r.pause_threshold = 0.7  # pause threshold


while True:
    with sr.Microphone(device_index=1) as source:
        print("Listening 🎙️")
        # audio = r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        
        transcript = r.recognize_whisper(audio)
        if transcript == "bye":
            exit(0)
            
        print("Thinking 🤔")
        print(f"😃: {transcript}")
        response = chat(question=transcript)
        
        print("Speaking 🔊")
        print(f"😺: {response}")
        tts(text=response)
