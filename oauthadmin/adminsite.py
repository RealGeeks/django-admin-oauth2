from django.contrib.admin.sites import AdminSite

from oauthadmin.views import login, logout_redirect

class OauthAdminSite(AdminSite):

    def login(self, request, extra_context=None):
        return login(request)

    def logout(self, request, extra_context=None):
        return logout_redirect(request)
