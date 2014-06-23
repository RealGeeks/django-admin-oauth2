import mock
import pytest
from oauthadmin.views import destroy_session, login, callback, logout
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, InvalidGrantError
from django.test.client import RequestFactory


SESSION_VARIABLES = ['oauth_state', 'oauth_token', 'uid', 'user']


@pytest.fixture
def request_factory():
    return RequestFactory()

def test_destroy_session(request_factory):
    request = request_factory.get('/')
    request.session = dict([(key, key) for key in SESSION_VARIABLES])
    assert destroy_session(request) == None
    assert isinstance(request.session, dict)
    assert request.session == {}

def test_destroy_session_with_extra_values(request_factory):
    request = request_factory.get('/')
    request.session = dict([(key, key) for key in SESSION_VARIABLES] + [('extra', 'extra')])
    assert destroy_session(request) == None
    assert isinstance(request.session, dict)
    assert request.session == {'extra': 'extra'}

def test_destroy_session_with_empty_values(request_factory):
    request = request_factory.get('/')
    request.session = {}
    assert destroy_session(request) == None
    assert isinstance(request.session, dict)
    assert request.session == {}


@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
def test_login(app_setting, OAuth2Session, request_factory):
    OAuth2Session.return_value = mock.Mock(
        authorization_url = mock.Mock(return_value = ('https://foo', 'state-variable'))
    )
    request = request_factory.post('/')
    request.session = {}
    request.build_absolute_uri = mock.Mock(return_value='https://test.com/construct-redirect')

    app_setting.return_value = 'app-setting'

    resp = login(request)
    assert resp.status_code == 302
    assert request.session.get('oauth_state') == 'state-variable'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback_with_mismatching_state(import_by_path, app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_state':'foo'}
    app_setting.return_value = 'app-setting'
    OAuth2Session.return_value = mock.Mock(fetch_token = mock.Mock(side_effect=MismatchingStateError))
    resp = callback(request)
    assert resp.status_code == 302
    assert resp['location'] == 'http://testserver/login/'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback_with_missing_state(import_by_path, app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {}
    app_setting.return_value = 'app-setting'
    resp = callback(request)
    assert resp.status_code == 302
    assert resp['location'] == 'http://testserver/login/'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback_with_invalid_grant(import_by_path, app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_state':'foo'}
    app_setting.return_value = 'app-setting'
    OAuth2Session.return_value = mock.Mock(fetch_token = mock.Mock(side_effect=InvalidGrantError))
    resp = callback(request)
    assert resp.status_code == 302
    assert resp['location'] == 'http://testserver/login/'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback(import_by_path, app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_state': 'state-variable'}
    OAuth2Session.return_value = mock.Mock(
        fetch_token = mock.Mock(return_value = 'token')
    )
    app_setting.return_value = 'app-setting'
    ibp = mock.Mock()
    ibp.return_value = 'test-user'
    import_by_path.return_value = ibp

    resp = callback(request)
    assert resp.status_code == 302
    assert request.session.get('oauth_token') == 'token'
    assert request.session.get('user') == 'test-user'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
def test_logout(app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_token': 'token'}
    app_setting.return_value = 'app-setting'
    resp = logout(request)
    assert resp.status_code == 302
    assert resp['Location'] == 'http://testserver/'
