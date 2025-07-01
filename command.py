from speech import speak
from ai import ai
import webbrowser
import os
import datetime
import random
import subprocess


INSTANT_COMMANDS = {
    "time": lambda: datetime.datetime.now().strftime("It's %I:%M %p"),
    "date": lambda: datetime.datetime.now().strftime("%A, %B %d"),
    "joke": lambda: random.choice([
        "Why don't scientists trust atoms? They make up everything!",
        "Parallel lines have so much in common... It's a shame they'll never meet."
    ]),
    "stop": lambda: os._exit(0)
}

# System apps
SYSTEM_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe"
}

def process_command(command: str):
    command = command.lower().strip()
    

    if command in INSTANT_COMMANDS:
        speak(INSTANT_COMMANDS[command]())
        return
    

    if command.startswith("launch "):
        app = command[7:]
        if app in SYSTEM_APPS:
            os.startfile(SYSTEM_APPS[app])
            speak(f"Launched {app}")
        else:
            speak("App not found")
        return
    
    # AI response
    if ai and ai.online:
        speak(ai.chat(command))
    else:
        speak("I'm offline. Try 'time', 'date', or 'launch' commands.")