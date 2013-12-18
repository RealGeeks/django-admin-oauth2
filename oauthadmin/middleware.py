class OauthAdminSessionMiddleware(object):
    def process_request(self, request):
        if hasattr(request, 'session') and 'user' in request.session:
            request.user = request.session['user']
            request._cached_user = request.session['user']
        else:
            from django.contrib.auth.models import AnonymousUser
            request.user = AnonymousUser()
