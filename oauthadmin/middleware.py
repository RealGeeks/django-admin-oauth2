from time import time
from oauthadmin.utils import import_by_path
from oauthadmin.settings import app_setting
from oauthadmin.views import destroy_session

class OauthAdminSessionMiddleware(object):
    def process_request(self, request):
        if hasattr(request, 'session') and 'user' in request.session:
            request.user = request.session['user']
            request._cached_user = request.session['user']

            if int(time()) - request.session.get('utctimestamp', 0) >= app_setting('PING_INTERVAL'):
                request.session['utctimestamp'] = int(time())
                is_valid = import_by_path(app_setting('PING'))(request.session['oauth_token'])
                if not is_valid:
                    destroy_session(request)

        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
