import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(Path(__file__).parent.parent.parent, '.env'))

BASE_DIR = Path(__file__).parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_HASH_ALGORITHM = os.environ.get('JWT_HASH_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30
