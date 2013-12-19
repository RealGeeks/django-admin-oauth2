import mock
from oauthadmin.views import destroy_session, login, callback, logout


SESSION_VARIABLES = ['oauth_state', 'oauth_token', 'uid', 'user']


def setup_module(mod):
    global request
    request = mock.Mock()
    request.session = {}
    request.GET = mock.Mock()
    request.GET.urlencode = mock.Mock()
    request.GET.urlencode.return_value = 'GET'
    request.POST = mock.Mock()
    request.POST.urlencode = mock.Mock()
    request.POST.urlencode.return_value = 'POST'

def teardown_module(mod):
    global request
    del request

def test_destroy_session():
    request.session = dict([(key, key) for key in SESSION_VARIABLES])
    assert destroy_session(request) == None
    assert isinstance(request.session, dict)
    assert request.session == {}

def test_destroy_session_with_extra_values():
    request.session = dict([(key, key) for key in SESSION_VARIABLES] + [('extra', 'extra')])
    assert destroy_session(request) == None
    assert isinstance(request.session, dict)
    assert request.session == {'extra': 'extra'}

def test_destroy_session_with_empty_values():
    request.session = {}
    assert destroy_session(request) == None
    assert isinstance(request.session, dict)
    assert request.session == {}

## L O G I N

def _mock_oauth2session(*_, **__):

    def _mock_authorization_url(*_, **__):
        return ('http://goatse.cx', 'state-variable')        

    def _mock_fetch_token(*_, **__):
        return 'token'

    x = mock.Mock()
    x.authorization_url = _mock_authorization_url
    x.fetch_token = _mock_fetch_token
    return x

def _mock_build_absolute_uri(*_, **__):
    return 'https://test.com/construct-redirect'

@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.OAuth2Session', new=_mock_oauth2session)
def test_login(app_setting):
    
    request.session = {}
    request.build_absolute_uri = _mock_build_absolute_uri

    app_setting.return_value = 'app-setting'

    resp = login(request)
    assert resp.status_code == 302
    assert request.session.get('oauth_state') == 'state-variable'

@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.import_by_path')
@mock.patch('oauthadmin.views.OAuth2Session', new=_mock_oauth2session)
def test_callback(import_by_path, app_setting):

    request.session = {'oauth_state': 'state-variable'}

    app_setting.return_value = 'app-setting'
    ibp = mock.Mock()
    ibp.return_value = 'test-user'
    import_by_path.return_value = ibp

    resp = callback(request)
    assert resp.status_code == 302
    assert request.session.get('oauth_token') == 'token'
    assert request.session.get('user') == 'test-user'

@mock.patch('oauthadmin.views.app_setting')
@mock.patch('oauthadmin.views.OAuth2Session', new=_mock_oauth2session)
def test_logout(app_setting):

    request.session = {'oauth_token': 'token'}
    request.build_absolute_uri = _mock_build_absolute_uri

    app_setting.return_value = 'app-setting'
    
    resp = logout(request)
    assert resp.status_code == 302