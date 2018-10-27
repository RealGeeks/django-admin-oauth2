from django.conf import settings as django_settings

# Default values for all django-oauth2-admin settings
DEFAULT_SETTINGS = {
    'GET_USER': 'oauthadmin.stubs.get_user',
    'PING_INTERVAL': 300,
    'OAUTHADMIN_DEFAULT_NEXT_URL': '/admin/',
}
OAUTHADMIN_SETTINGS_PREFIX = 'OAUTHADMIN_'


def app_setting(name):
    return getattr(
        django_settings,
        '{}{}'.format(OAUTHADMIN_SETTINGS_PREFIX, name),
        DEFAULT_SETTINGS.get(name)
    )
