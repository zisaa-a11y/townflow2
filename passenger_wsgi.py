import sys
import os
import traceback

# Set debug to true to see errors
os.environ['DEBUG'] = 'True'

sys.path.insert(0, '/home/riveygjm/townflow.riverviewpabna.com')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
