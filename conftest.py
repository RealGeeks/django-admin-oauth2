import django

def pytest_configure():
    if hasattr(django, 'setup'):
        django.setup()
