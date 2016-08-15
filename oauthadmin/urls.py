from django.conf.urls import url
import oauthadmin.views

urlpatterns = [
    url(r'login/', oauthadmin.views.login),
    url(r'callback/', oauthadmin.views.callback),
    url(r'logout/', oauthadmin.views.logout),
    url(r'logout_redirect/', oauthadmin.views.logout_redirect),
]
