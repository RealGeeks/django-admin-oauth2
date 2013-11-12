from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'login/', 'oauthadmin.views.login'),
)
