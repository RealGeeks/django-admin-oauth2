from django.conf import settings

settings.configure(
	CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache',}},
)

from django.test import TestCase
from mock import Mock
from oauthadmin.middleware import OauthAdminSessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.test.utils import override_settings

from django.conf import settings

def setup_module(mod):
    mod.mw = OauthAdminSessionMiddleware()
    mod.request = Mock()
    mod.request.session = {}

def test_process_request_with_user():
	data = {'id': 1}
	request.session = {'user': data}
	assert mw.process_request(request) is None
	assert isinstance(request.user, dict)
	print request.user
	assert request.user.get('id') is data['id']

def test_process_request_without_user():
	request.session = {}
	assert mw.process_request(request) is None
	assert isinstance(request.user, AnonymousUser)