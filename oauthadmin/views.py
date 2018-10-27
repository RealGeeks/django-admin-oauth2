from time import time
import base64
import json

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError, InvalidGrantError
from oauthlib.common import generate_token
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from oauthadmin.utils import import_by_path
from oauthadmin.settings import app_setting
import oauthadmin.views

try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch



def destroy_session(request):

    # These session variables MAY not exist at this point.
    for key in ['oauth_state', 'oauth_token', 'uid', 'user','last_verified_at']:
        try:
            del request.session[key]
        except KeyError:
            pass

def login(request):
    # this view can be called directly by django admin site from
    # any url, or can be accessed by the login url if the urls
    # from this app were included
    if request.path == reverse(oauthadmin.views.login):
        # if this view is being accessed from login url look for 'next'
        # in query string to use as destination after the login is complete
        next = request.GET.get('next')
    else:
        # otherwise the django admin site called this view from another view.
        # Django admin doesn't redirect to login url if login is required, it
        # calls the view directly (django 1.7 fixed this and redirects and we
        # don't support it yet)
        next = request.get_full_path()

    redirect_uri = request.build_absolute_uri(reverse(oauthadmin.views.callback))
    state_token = generate_token()
    state=base64.b64encode(json.dumps({"state": state_token, "next": next}).encode('utf-8'))
    oauth = OAuth2Session(
        client_id=app_setting('CLIENT_ID'),
        redirect_uri=redirect_uri,
        scope=app_setting('SCOPE'),
        state=state,
    )
    authorization_url, state = oauth.authorization_url(app_setting('AUTH_URL'))

    request.session['oauth_state'] = state

    return redirect(authorization_url)


def callback(request):
    if 'oauth_state' not in request.session:
        return HttpResponseRedirect(request.build_absolute_uri(reverse(oauthadmin.views.login)))
    redirect_uri = request.build_absolute_uri(reverse(oauthadmin.views.callback))
    oauth = OAuth2Session(
        app_setting('CLIENT_ID'),
        state=request.session['oauth_state'].decode('utf-8'),
        redirect_uri=redirect_uri,
    )
    try:
        token = oauth.fetch_token(
            app_setting('TOKEN_URL'),
            client_secret=app_setting('CLIENT_SECRET'),
            authorization_response=app_setting('AUTH_URL') + "?" + request.GET.urlencode()
        )
    except (MismatchingStateError, InvalidGrantError):
        return HttpResponseRedirect(request.build_absolute_uri(reverse(oauthadmin.views.login)))

    user = import_by_path(app_setting('GET_USER'))(token)

    request.session['last_verified_at'] = int(time())
    request.session['oauth_token'] = token
    request.session['user'] = user

    next = json.loads(base64.b64decode(request.session['oauth_state']).decode('utf-8'))['next']
    if not next:
        next = app_setting('DEFAULT_NEXT_URL')

    return redirect(request.build_absolute_uri(next))


def logout(request):
    if 'oauth_token' in request.session:
        oauth = OAuth2Session(app_setting('CLIENT_ID'), token=request.session['oauth_token'])
        oauth.get(app_setting('BASE_URL') + 'destroy_tokens')

        destroy_session(request)

    return redirect(request.build_absolute_uri('/'))


def logout_redirect(request):
    return redirect(app_setting('BASE_URL') + 'logout?next=' + quote_plus(request.build_absolute_uri(reverse(oauthadmin.views.logout))))
