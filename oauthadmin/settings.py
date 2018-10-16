from django.conf import settings as global_settings

defaults = {
    # default values for all django-oauth2-admin settings
    "GET_USER": 'oauthadmin.utils.get_user',
    "PING_INTERVAL": 300,
    "DEFAULT_NEXT_URL": "/admin/",
    "SCOPE": ['default'],
    "GROUPS": [],
}

global_prefix = 'OAUTHADMIN_'


def app_setting(name):
    return getattr(global_settings, global_prefix+name, defaults.get(name))
