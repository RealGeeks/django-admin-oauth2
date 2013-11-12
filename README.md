# django-admin-oauth2

A django app that replaces the django admin authentication mechanism by
deferring to an oauth2 provider.


## Installation

1. Include the django-admin-oauth2 urlconf in your project's urls.py:

```python
url(r'/admin/oauth/', include('oauthadmin.urls'))
```

2. Install the middleware in your project's settings.py:

```python
MIDDLEWARE_CLASSES = (
    'oauthadmin.middleware.OauthAdminMiddleware'
)

```
3. Set up all the correct options (see below for available options)

## Settings

 * OAUTHADMIN_GET_USER: This is function that is given the oauth token and returns
   a django.auth.models.User model corresponding to the currently logged-in user.
   You can set permissions on this user object and stuff.
