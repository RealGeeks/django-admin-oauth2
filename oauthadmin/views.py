from time import time

from requests_oauthlib import OAuth2Session
from urllib import quote_plus

from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from oauthadmin.utils import import_by_path
from oauthadmin.settings import app_setting


def destroy_session(request):

    # These session variables MAY not exist at this point.
    for key in ['oauth_state', 'oauth_token', 'uid', 'user']:
        try:
            del request.session[key]
        except KeyError:
            pass

def login(request):
    oauth = OAuth2Session(
        client_id=app_setting('CLIENT_ID'),
        redirect_uri=request.build_absolute_uri(reverse('oauthadmin.views.callback')),
        scope=["default"],
    )
    authorization_url, state = oauth.authorization_url(app_setting('AUTH_URL'))

    request.session['oauth_state'] = state

    return redirect(authorization_url)


def callback(request):
    oauth = OAuth2Session(app_setting('CLIENT_ID'), state=request.session['oauth_state'])
    token = oauth.fetch_token(
        app_setting('TOKEN_URL'),
        client_secret=app_setting('CLIENT_SECRET'),
        authorization_response=app_setting('AUTH_URL') + "?" + request.GET.urlencode()
    )

    user = import_by_path(app_setting('GET_USER'))(token)

    request.session['utctimestamp'] = int(time())
    request.session['oauth_token'] = token
    request.session['user'] = user

    return redirect(request.build_absolute_uri('/admin'))
    

def logout(request):


    if 'oauth_token' in request.session:
        oauth = OAuth2Session(app_setting('CLIENT_ID'), token=request.session['oauth_token'])
        oauth.get(app_setting('BASE_URL') + 'destroy_tokens')

        destroy_session(request)

    return redirect(request.build_absolute_uri('/'))


def logout_redirect(request):
    return redirect(app_setting('BASE_URL') + 'logout?next=' + quote_plus(request.build_absolute_uri(reverse('oauthadmin.views.logout'))))
