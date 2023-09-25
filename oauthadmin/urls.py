from django.urls import re_path
import oauthadmin.views

urlpatterns = [
    re_path(r'login/', oauthadmin.views.login),
    re_path(r'callback/', oauthadmin.views.callback),
    re_path(r'logout/', oauthadmin.views.logout),
    re_path(r'logout_redirect/', oauthadmin.views.logout_redirect),
]
