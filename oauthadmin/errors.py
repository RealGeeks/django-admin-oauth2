class OAuthAdminException(Exception):
    pass


class UnauthorizedUser(OAuthAdminException):
    pass
