import sys
import os

# Add the project directory to Python path
# Update this path to match your Namecheap hosting directory
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Load .env file using django-environ
import environ
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), ".env"))

# Get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
