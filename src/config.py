import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_URI = os.getenv('DB_URI')

FRONTEND_URL = os.getenv('FRONTEND_URL')