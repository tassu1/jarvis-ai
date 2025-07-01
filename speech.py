import speech_recognition as sr
import pyttsx3
import asyncio

# Initialize
engine = pyttsx3.init()
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.3  
recognizer.non_speaking_duration = 0.2

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

async def listen():
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(
                source, 
                timeout=1, 
                phrase_time_limit=3
            )
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            return ""
        except:
            return None