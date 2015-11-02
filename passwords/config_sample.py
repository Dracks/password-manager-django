__author__ = 'dracks'

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'devel.sqlite3'),
    }
}

cors = (
        'localhost:4200',
    )