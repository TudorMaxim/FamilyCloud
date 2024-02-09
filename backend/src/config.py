import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_USER = os.getenv('DEFAULT_USER')
DATABASE_URL = os.getenv('DATABASE_URL')
