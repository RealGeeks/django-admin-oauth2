# django-admin-oauth2

A django app that replaces the django admin authentication mechanism by
deferring to an oauth2 provider.

[![Build Status](https://travis-ci.org/RealGeeks/django-admin-oauth2.png?branch=master)](https://travis-ci.org/RealGeeks/django-admin-oauth2)

# Support

django-admin-oauth2 should support Python 2.7 & Python 3.6 to 3.11, pypy, and Django versions 1.6 through 4

## Installation

Step 1: `pip install django-admin-oauth2` and include it in your project's requirements

Step 2: Include the django-admin-oauth2 urlconf in your project's urls.py:

Django 1.x

```python
url(r'/admin/oauth/', include('oauthadmin.urls'))
```

Django >= 2.0

```python
re_path(r'/admin/oauth/', include('oauthadmin.urls'))
```

Step 3: Include oauthadmin in your INSTALLED_APPS:

```python
INSTALLED_APPS = (
    'oauthadmin'
)
```

Step 4: Install the middleware in your project's settings.py:

```python
MIDDLEWARE_CLASSES = (
    'oauthadmin.middleware.OauthAdminSessionMiddleware'
)
```

_make sure that this comes AFTER 'django.contrib.sessions.middleware.SessionMiddleware'_

Step 5: Set up all the correct options (see below for available options)

## Settings

- OAUTHADMIN_GET_USER: This is function that is given the oauth token and returns
  a django.auth.models.User model corresponding to the currently logged-in user.
  You can set permissions on this user object and stuff.
- OAUTHADMIN_CLIENT_ID: Your oAuth client ID
- OAUTHADMIN_CLIENT_SECRET: oAuth client secret
- OAUTHADMIN_BASE_URL: The landing point for all oAuth related queries.
- OAUTHADMIN_AUTH_URL: oAuth provider URL
- OAUTHADMIN_TOKEN_URL: oAuth bearer token provider URL
- OAUTHADMIN_PING_INTERVAL (optional, defaults to 300): Minimum number of seconds between ping requests
- OAUTHADMIN_PING: (optional, defaults to None) This optional function takes an oauth token and returns True if it's still valid and False if it's no longer valid (if they have logged out of the oauth server)
- OAUTHADMIN_DEFAULT_NEXT_URL: (optional, defaults to /admin). This optional value is the default page that a successful oauth login process will land you on.
- OAUTHADMIN_SCOPE: (optional, defaults to ['default']). This is a list of authorization scopes.

## Testing

If you want to test this app, please run the following `Makefile` command:

```
make test
```

## Notes

When the CSRF validation token doesn't match, django-admin-oauth2 will redirect back to the login url so it can retry the authorization step. Sometimes people will bookmark the oauth server with an out-of-date CSRF state string, this is better than showing them an error page.

## Changelog

- 1.3.0: Add support for `JSONSerializer`
- 1.2.1: Add support for django 4, retain backwards compat with Django 1.x
- 1.2.0: Allow overriding oauth scope with new parameter, OAUTHADMIN_SCOP
- 1.1.3: Bugfix in adminsite (tabs vs spaces)
- 1.1.2: Add support for django 2
- 1.1.1: Fix a bug where the new setting wasn't getting read
- 1.1.0: Add new setting: OAUTHADMIN_DEFAULT_NEXT_URL
- 1.0.2: Support python3
- 1.0.1: Send redirect URI when exchanging grant code for auth token
- 1.0.0: Add support for django 1.8, 1.9, and 1.10. Drop support for python 2.6. Add support for python 3.5. Update test suite to run with tox.
- 0.2.6: Roundtrip original URL accessed through the oauth process so you can go to the URL you requested after the authorization process finishes. Thanks @igorsobreira.
- 0.2.5: Fix bug where failing ping was not invalidating session immediately, only on the second request.
- 0.2.4: Redirect to the login if the grant is invalid
- 0.2.3: Redirect to the login if the state is mismatching
- 0.2.2: Redirect to the login if the state goes missing (sometimes people bookmark the login url)
- 0.2.1: Added tests for the ping function and fixed a bug with the session variable name for the ping timestamp.
- 0.2.0: Added support for pinging the auth server to make sure the token is still valid
