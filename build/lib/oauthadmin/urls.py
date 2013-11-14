from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'login/', 'oauthadmin.views.login'),
    (r'callback/', 'oauthadmin.views.callback'),
    (r'logout/', 'oauthadmin.views.logout'),
    (r'logout_redirect/', 'oauthadmin.views.logout_redirect'),
)
