# Password manager using django
It's a password manager like Team Password using django and [ember-js](https://github.com/Dracks/password-manager-emberjs)

It's a simple project to learn django and emberjs, obtaining a tool that I require in a moment concrete, and teampass 
don't work on my computer. 

## Requirements
The following libraries are required

* Django 
* django-cors-headers 
* djangorestframework 
* djangorestframework-jwt 
* django-mptt 
* django-filter
  

## Installation

## Apache Configuration

WSGI Script  (I've got a venv folder that is a virtual environment with the dependencies installed)
```python
import os, sys

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
workspace = os.path.dirname(apache_configuration)
activate_this=apache_configuration+'/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(apache_configuration) 

#Add the path to 3rd party django application and to django itself.

#os.environ['DJANGO_SETTINGS_MODULE'] = 'dj_project.apache.settings_production'
os.environ['DJANGO_SETTINGS_MODULE'] = 'passwords.settings'
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

