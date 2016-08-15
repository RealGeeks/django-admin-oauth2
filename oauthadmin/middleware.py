from time import time
from oauthadmin.utils import import_by_path
from oauthadmin.settings import app_setting
from oauthadmin.views import destroy_session

try:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-middleware
    from django.utils.deprecation import MiddlewareMixin
    BaseClass = MiddlewareMixin
except ImportError:
    BaseClass = object

def _ping_timeout_expired(timestamp, ping_interval):
    return time() - timestamp > ping_interval

def _verify_ping_interval(request, ping_interval, ping_func):
    if not _ping_timeout_expired(
        ping_interval,
        request.session.get('last_verified_at', 0),
    ):
        return
    request.session['last_verified_at'] = int(time())
    is_valid = ping_func(request.session['oauth_token'])
    if not is_valid:
        destroy_session(request)
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

class OauthAdminSessionMiddleware(BaseClass):
    def process_request(self, request):
        if hasattr(request, 'session') and 'user' in request.session:
            request.user = request.session['user']
            request._cached_user = request.session['user']

            if app_setting('PING_INTERVAL') and app_setting('PING'):
                _verify_ping_interval(
                    request,
                    app_setting('PING_INTERVAL'),
                    import_by_path(app_setting('PING'))
                )

        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
