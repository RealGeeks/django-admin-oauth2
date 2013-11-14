from django.contrib.admin.sites import AdminSite
# from django.shortcuts import redirect
# from django.core.urlresolvers import reverse

from oauthadmin.views import login, logout_redirect

class OauthAdminSite(AdminSite):

	login = login
	logout = logout_redirect

	# def login(self, request, extra_context=None):
	# 	return redirect(reverse('oauthadmin.views.login'))

	# def logout(self, request, extra_context=None):
	# 	return redirect(reverse('oauthadmin.views.logout_redirect'))
