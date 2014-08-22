from mock import Mock
from freezegun import freeze_time
from django.contrib.auth.models import AnonymousUser
from django.test.utils import override_settings
from oauthadmin.middleware import OauthAdminSessionMiddleware

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


false_mock_pinger = Mock(return_value = False)

@override_settings(OAUTHADMIN_PING_INTERVAL=5)
@override_settings(OAUTHADMIN_PING='test.test_middleware.false_mock_pinger')
def test_that_anonymoususer_goes_in_request_user_if_ping_fails():
    request.session = {'user':'not anonymous', 'oauth_token':'abc'}
    request.user = 'not anonymous'
    mw.process_request(request)
    assert isinstance(request.user, AnonymousUser)


mock_pinger = Mock()

@override_settings(OAUTHADMIN_PING_INTERVAL=5)
@override_settings(OAUTHADMIN_PING='test.test_middleware.mock_pinger')
def test_process_request_with_reverify_interval():
    request.session = {'oauth_token': 1234, 'user':1234}
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
