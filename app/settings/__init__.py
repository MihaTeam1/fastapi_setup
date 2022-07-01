import os
import sys
from os.path import join
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(join(Path(__file__).parent.parent.parent, '.env'))

module = os.environ.get("SETTINGS_MODULE")
if module == 'production':
    from .production import *
else:
    from .development import *
