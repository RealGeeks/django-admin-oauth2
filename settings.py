CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}

ROOT_URLCONF = "oauthadmin.urls"
SECRET_KEY = "secret"
ALLOWED_HOSTS = ['testserver']

OAUTHADMIN_CLIENT_ID = 'test-client-id'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth'
]
