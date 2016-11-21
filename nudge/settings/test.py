import os
import os.path


BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')


SECRET_KEY=os.urandom(32)
ROOT_URLCONF='hello.urls'


ZAPPA_SETTINGS = {
    'test': {
        'project_name': 'hello',
        'aws_region': 'eu-west-1',
        's3_bucket': 'template-zappa-hello',
        'settings_file': os.path.join(BASE_DIR, 'hello', 'settings/' 'test.py'),
    },
}


INSTALLED_APPS = [
    'django_zappa',
]


ALLOWED_HOSTS = ['*',]
