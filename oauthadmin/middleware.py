from django.conf import settings as dj_settings


class OauthAdminSessionMiddleware(object):
    def process_request(self,request):
        if not hasattr(request,' session'):
            raise Exception("Make sure you put the OuathAdminmiddleware *after* the django session middleware"
        if 'user' in request.session:
            request.user = request.session['user']
            request._cached_user = request.session['user']
