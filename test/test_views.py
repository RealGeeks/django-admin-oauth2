import mock
import pytest
import base64
import json
from oauthadmin.views import destroy_session, login, callback, logout
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, InvalidGrantError
from django.test.client import RequestFactory
from django.contrib.auth.models import User
import oauthadmin.views

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


SESSION_VARIABLES = ['oauth_state', 'oauth_token', 'uid', 'user']


def _state(token, next=None):
    return base64.b64encode(json.dumps({'state': token, 'next': next or ''}).encode('utf-8'))

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
        authorization_url = mock.Mock(return_value = ('https://foo', _state('state-variable')))
    )
    request = request_factory.get(reverse(oauthadmin.views.login))
    request.session = {}
    request.build_absolute_uri = mock.Mock(return_value='https://test.com/construct-redirect')

    app_setting.return_value = 'app-setting'

    resp = login(request)
    assert resp.status_code == 302
    assert resp['location'] == 'https://foo'
    assert request.session.get('oauth_state') == _state('state-variable').decode('utf-8')

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.generate_token')
def test_login_redirect_uri(generate_token, OAuth2Session, request_factory):
    OAuth2Session.return_value = mock.Mock(
        authorization_url = mock.Mock(return_value = ('https://foo', _state('state-variable')))
    )
    generate_token.return_value = '1234'
    request = request_factory.get(reverse(oauthadmin.views.login))
    request.session = {}
    request.build_absolute_uri = mock.Mock(return_value='https://test.com/construct-redirect')

    resp = login(request)

    OAuth2Session.assert_called_once_with(
        client_id = 'test-client-id',
        redirect_uri = u'https://test.com/construct-redirect',
        scope = ['default'],
        state = base64.b64encode(json.dumps({"state": '1234', "next": None}).encode('utf-8')),
    )

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.generate_token')
def test_login_redirect_uri_with_next_from_url(generate_token, OAuth2Session, request_factory):
    OAuth2Session.return_value = mock.Mock(
        authorization_url = mock.Mock(return_value = ('https://foo', _state('state-variable')))
    )
    generate_token.return_value = '1234'
    request = request_factory.get(reverse(oauthadmin.views.login) + '?next=/admin/content/')
    request.session = {}
    request.build_absolute_uri = mock.Mock(return_value='https://test.com/construct-redirect')

    resp = login(request)

    OAuth2Session.assert_called_once_with(
        redirect_uri = u'https://test.com/construct-redirect',
        client_id = mock.ANY,
        scope = mock.ANY,
        state = base64.b64encode(json.dumps({"state": '1234', "next": '/admin/content/'}).encode('utf-8')),
    )

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.generate_token')
def test_login_redirect_uri_with_next_as_current_url(generate_token, OAuth2Session, request_factory):
    OAuth2Session.return_value = mock.Mock(
        authorization_url = mock.Mock(return_value = ('https://foo', _state('state-variable')))
    )
    generate_token.return_value = '1234'
    request = request_factory.get('/admin/content/')
    request.session = {}
    request.build_absolute_uri = mock.Mock(return_value='https://test.com/construct-redirect')

    resp = login(request)

    OAuth2Session.assert_called_once_with(
        redirect_uri = u'https://test.com/construct-redirect',
        client_id = mock.ANY,
        scope = mock.ANY,
        state = base64.b64encode(json.dumps({"state": '1234', "next": '/admin/content/'}).encode('utf-8')),
    )


@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback_with_mismatching_state(import_by_path, app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_state':_state('foo')}
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
    request.session = {'oauth_state':_state('foo')}
    app_setting.return_value = 'app-setting'
    OAuth2Session.return_value = mock.Mock(fetch_token = mock.Mock(side_effect=InvalidGrantError))
    resp = callback(request)
    assert resp.status_code == 302
    assert resp['location'] == 'http://testserver/login/'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.serializers.serialize')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback(import_by_path, mock_serialized_json_user, app_setting, OAuth2Session, request_factory):
    request = request_factory.get(reverse(oauthadmin.views.callback))
    request.session = {'oauth_state': _state('state-variable')}
    OAuth2Session.return_value = mock.Mock(
        fetch_token = mock.Mock(return_value = 'token')
    )
    app_setting.return_value = 'app-setting'
    ibp = mock.Mock()
    ibp.return_value = User(id=1)
    import_by_path.return_value = ibp

    serialized_user = '[{"model": "auth.user", "pk": 1, "fields": {}}]'
    mock_serialized_json_user.return_value = serialized_user

    resp = callback(request)
    assert resp.status_code == 302
    assert resp['location'] == 'http://testserver/callback/app-setting'
    assert request.session.get('oauth_token') == 'token'
    mock_serialized_json_user.assert_called_once_with("json", [User(id=1)])
    assert request.session.get('user') == serialized_user

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.serializers.serialize')
@mock.patch('oauthadmin.views.import_by_path')
def test_callback_redirect_to_next(import_by_path, mock_serialized_json_user, app_setting, OAuth2Session, request_factory):
    request = request_factory.get(reverse(oauthadmin.views.callback))
    request.session = {'oauth_state': _state('state-variable','/admin/content/')}
    OAuth2Session.return_value = mock.Mock(
        fetch_token = mock.Mock(return_value = 'token')
    )
    app_setting.return_value = 'app-setting'
    ibp = mock.Mock()
    ibp.return_value = User(id=1)
    import_by_path.return_value = ibp

    serialized_user = '[{"model": "auth.user", "pk": 1, "fields": {}}]'
    mock_serialized_json_user.return_value = serialized_user

    resp = callback(request)
    
    mock_serialized_json_user.assert_called_once_with("json", [User(id=1)])
    assert request.session.get('user') == serialized_user

    assert resp.status_code == 302
    assert resp['location'] == 'http://testserver/admin/content/'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
def test_logout_redirects(app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_token': 'token'}
    app_setting.return_value = 'app-setting'
    resp = logout(request)
    assert resp.status_code == 302
    assert resp['Location'] == 'http://testserver/'

@mock.patch('oauthadmin.views.OAuth2Session')
@mock.patch('oauthadmin.views.app_setting')
def test_logout_destroys_session(app_setting, OAuth2Session, request_factory):
    request = request_factory.get('/')
    request.session = {'oauth_token': 'token'}
    app_setting.return_value = 'app-setting'
    assert request.session.get('oauth_token') == 'token'
    resp = logout(request)
    assert request.session.get('oauth_token') == None
