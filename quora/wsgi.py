import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/manhee/interface/')
sys.path.append('/home/manhee/interface/quora')
sys.path.append('/home/manhee/interface/quora/quora')
sys.path.append('/home/manhee/interface/venv/lib/python3.7/site-packages')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quora.settings')

application = get_wsgi_application()
