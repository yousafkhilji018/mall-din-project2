"""
WSGI config for super_store project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'super_store.settings')

application = get_wsgi_application()

# Vercel: create tables in /tmp sqlite on cold start
if os.environ.get('VERCEL'):
    try:
        from django.core.management import call_command
        call_command('migrate', run_syncdb=True, verbosity=0, interactive=False)
    except Exception:
        pass
