from mock import Mock
from oauthadmin.middleware import OauthAdminSessionMiddleware
from django.contrib.auth.models import AnonymousUser

def setup_module(mod):
   global mw
   global request
   mw = OauthAdminSessionMiddleware()
   request = Mock()
   request.session = {}

def teardown_module(mod):
   global mw
   global request
   del mw
   del request

def test_process_request_without_user():
    request.session = {}
    assert mw.process_request(request) is None
    assert isinstance(request.user, AnonymousUser)

def test_process_request_with_user():
    data = {'id': 1}
    request.session = {'user': data}
    assert mw.process_request(request) is None
    assert isinstance(request.user, dict)
    assert request.user.get('id') is data['id']