from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings

import MySQLdb

class InfoConfig(AppConfig):
    name = 'info'




def dbconn():
    
    return MySQLdb.connect(host=settings.DATABASES['default']['HOST'],
                          	 db=settings.DATABASES['default']['NAME'],
                           user=settings.DATABASES['default']['USER'],
                         passwd=settings.DATABASES['default']['PASSWORD'],
                           port=settings.DATABASES['default']['PORT'])