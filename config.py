import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CAL_API_KEY = os.getenv('CAL_API_KEY')
    CAL_API_URL= os.getenv('CAL_API_URL')