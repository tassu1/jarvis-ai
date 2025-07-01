import asyncio
from speech import listen, speak
from command import process_command
from ai import ai
import logging

class Assistant:
    def __init__(self):
        self.wake_words = ["robin", "computer"]
        self.active = False

    async def run(self):
        speak("Ready" if ai and ai.online else "Offline mode")
        while True:
            await self.listen_loop()

    async def listen_loop(self):
        try:
            text = await listen()
            if not text:
                return

            if any(wake_word in text.lower() for wake_word in self.wake_words):
                self.active = True
                speak("Yes?")
                await self.command_loop()
                
        except Exception as e:
            logging.error(f"Error: {str(e)}")

    async def command_loop(self):
        while self.active:
            command = await listen()
            if not command:
                continue
                
            if "stop" in command:
                self.active = False
                speak("Going to sleep")
                break
                
            await asyncio.to_thread(process_command, command)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    assistant = Assistant()
    asyncio.run(assistant.run())