# django-admin-oauth2

A django app that replaces the django admin authentication mechanism by
deferring to an oauth2 provider.


## Installation

1. Include the django-admin-oauth2 urlconf in your project's urls.py:

```python
url(r'/admin/oauth/', include('oauthadmin.urls'))
```

2. Include oauthadmin in your INSTALLED_APPS:

```python
INSTALLED_APPS = (
    'oauthadmin'
)
````


3. Install the middleware in your project's settings.py:

```python
MIDDLEWARE_CLASSES = (
    'oauthadmin.middleware.OauthAdminSessionMiddleware'
)
```

4. If you are on Django 1.5 or above, you'll need to set your session serializer
to "django.contrib.sessions.serializers.PickleSerializer" since we are storing the
pickled user object in the session.

```python
SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

```



 *make sure that this comes BEFORE 'django.contrib.sessions.middleware.SessionMiddleware'*

4. Set up all the correct options (see below for available options)

## Settings

 * OAUTHADMIN_GET_USER: This is function that is given the oauth token and returns
   a django.auth.models.User model corresponding to the currently logged-in user.
   You can set permissions on this user object and stuff.
 * OAUTHADMIN_CLIENT_ID: Your oAuth client ID
 * OAUTHADMIN_CLIENT_SECRET: oAuth client secret
 * OAUTHADMIN_BASE_URL: The landing point for all oAuth related queries.
 * OATHADMIN_AUTH_URL: oAuth provider URL
 * OAUTHADMIN_TOKEN_URL: oAuth bearer token provider URL
