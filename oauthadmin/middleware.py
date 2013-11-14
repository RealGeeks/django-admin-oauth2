from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings as dj_settings

def _starts_with_list(str, list):
    for item in list:
        if str.startswith(item):
            return True
    return False

class OauthAdminSessionMiddleware(object):
    def process_request(self,request):
        SessionMiddleware().process_request(request)
        if 'user' in request.session:
            request.user = request.session['user']
            request._cached_user = request.session['user']
