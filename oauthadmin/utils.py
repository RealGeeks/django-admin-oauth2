from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from importlib import import_module

from oauthadmin.settings import app_setting


# Note: This is a copy-paste from django 1.6 for backwards-compat reasons


def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImproperlyConfigured if something goes wrong.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
            error_prefix, dotted_path))

    module = import_module(module_path)

    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
            error_prefix, module_path, class_name))
    return attr


def apply_groups(user):
    for group_name in app_setting('GROUPS'):
        try:
            group = Group.objects.get(name=group_name)
            group.user_set.add(user)
        except Group.DoesNotExist:
            pass


def get_user(token):
    user_name = token['user_name']
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        user = User(username=user_name)
        user.is_superuser = False
        user.is_staff = True
        user.email = user_name
        user.first_name = token['full_name']
        user.save()
        apply_groups(user)
    return user
