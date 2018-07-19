import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','TvFind.settings')

import django
django.setup()

from django.db import IntegrityError

from showsearch.models import TvShow
a = TvShow(name='Joey')
try:
    a.save()
except IntegrityError:
    print('error')
