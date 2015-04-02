"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ['LD_LIBRARY_PATH'] = '/usr/lib/oracle/11.2/client64/lib/'
os.environ['ORACLE_HOME'] = '/usr/lib/oracle/11.2/client64/'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
