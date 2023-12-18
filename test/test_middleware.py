from mock import Mock
import json
from freezegun import freeze_time
from django.contrib.auth.models import AnonymousUser, User
from django.test.utils import override_settings
from oauthadmin.middleware import OauthAdminSessionMiddleware

def setup_module(mod):
   global mw
   global request
   mw = OauthAdminSessionMiddleware(Mock())
   request = Mock()
   request.session = {}

def teardown_module(mod):
   global mw
   global request
   del mw
   del request

# Note: We are not actually serializing the User
# as this required adding a database Engine.
MOCK_SERIALIZED_USER_DATA = json.dumps([{"model": "auth.user", "pk": 1, "fields": {}}])

def test_process_request_without_user():
    request.session = {}
    assert mw.process_request(request) is None
    assert isinstance(request.user, AnonymousUser)

def test_process_request_with_user():
    request.session = {'user': MOCK_SERIALIZED_USER_DATA}
    assert mw.process_request(request) is None
    assert isinstance(request.user, User)
    assert request.user.id == 1
    assert request._cached_user.id == 1


false_mock_pinger = Mock(return_value = False)

@override_settings(OAUTHADMIN_PING_INTERVAL=5)
@override_settings(OAUTHADMIN_PING='test.test_middleware.false_mock_pinger')
def test_that_anonymoususer_goes_in_request_user_if_ping_fails():
    request.user = User(id=1) # non anonymous user
    request.session = {
        'user': MOCK_SERIALIZED_USER_DATA, # non anonymous user
        'oauth_token':'abc'
    }
    mw.process_request(request)
    assert isinstance(request.user, AnonymousUser)


mock_pinger = Mock()

@override_settings(OAUTHADMIN_PING_INTERVAL=5)
@override_settings(OAUTHADMIN_PING='test.test_middleware.mock_pinger')
def test_process_request_with_reverify_interval():
    request.session = {'oauth_token': 1234, 'user': MOCK_SERIALIZED_USER_DATA}
    with freeze_time('2012-08-29 00:00:00'):
        # first request should set timestamp
        # and verify with pinger.
        mw.process_request(request)
        assert mock_pinger.called
        mock_pinger.called = False
    with freeze_time('2012-08-29 00:00:01'):
        # second request should not call pinger
        mw.process_request(request)
        assert not mock_pinger.called
    with freeze_time('2012-08-29 00:01:01'):
        # third request, after the ping interval
        # has passed, should call pinger.
        mw.process_request(request)
        assert mock_pinger.called
