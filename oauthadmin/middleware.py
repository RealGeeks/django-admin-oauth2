from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings as dj_settings

def _starts_with_list(str, list):
    for item in list:
        if str.startswith(item):
            return True
    return False

class AdminSessionMiddleware(object):
    def process_request(self,request):
        if _starts_with_list(request.path, dj_settings.ADMIN_SESSION_URLS):
            SessionMiddleware().process_request(request)
            if 'user' in request.session:
                request.user = request.session['user']
            else:
                AuthenticationMiddleware().process_request(request)
        return None

    def process_response(self,request,response):
        if _starts_with_list(request.path, dj_settings.ADMIN_SESSION_URLS):
            SessionMiddleware().process_response(request,response)
        return response
