import requests
import logging
import os
import time
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

class PersonalAI:
    def __init__(self):
        self.session = self._create_session()
        self.model = "gpt2"  
        self.conversation = []
        self.api_key = os.getenv('HF_API_KEY')
        self.online = self._check_api_status()
        
    def _create_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=1,  
            backoff_factor=0.5,
            status_forcelist=[408, 429, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        return session

    def _check_api_status(self) -> bool:
        try:
            response = self.session.get(
                "https://api-inference.huggingface.co/status",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False

    def chat(self, message: str) -> str:
        if not self.online:
            return "I'm offline right now."
            
        try:
            start_time = time.time()
            response = self.session.post(
                f"https://api-inference.huggingface.co/models/{self.model}",
                json={"inputs": message},
                timeout=3  
            )
            
            if response.status_code == 200:
                return response.json()[0]['generated_text']
            return "I couldn't process that quickly enough."
        except Exception as e:
            logging.error(f"AI Error: {str(e)}")
            return "Let's try that again."


try:
    ai = PersonalAI()
except:
    ai = None