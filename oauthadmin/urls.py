import oauthadmin.views

try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url


urlpatterns = [
    url(r"login/", oauthadmin.views.login),
    url(r"callback/", oauthadmin.views.callback),
    url(r"logout/", oauthadmin.views.logout),
    url(r"logout_redirect/", oauthadmin.views.logout_redirect),
]
