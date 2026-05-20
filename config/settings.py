import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, '.env'))
except ImportError:
    pass

# Use production settings
from config.production_settings import *

# Override with environment variables if needed
if os.environ.get('DEBUG'):
    DEBUG = os.environ.get('DEBUG') == 'True'
