import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(Path(__file__).parent.parent.parent, '.env'))

module = os.environ.get("SETTINGS_MODULE")

from .base import *

if module == 'production':
    from .production import *
else:
    from .development import *
