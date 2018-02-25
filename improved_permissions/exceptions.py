"""permissions exceptions"""
class ImproperlyConfigured(Exception):
    pass


class ModelNotDefined(Exception):
    pass


class ParentNotFound(Exception):
    pass


class PermissionNotFound(Exception):
    pass


class RoleNotFound(Exception):
    pass


class InvalidRoleAssignment(Exception):
    pass


class BadRoleArguments(Exception):
    pass


class NotAllowed(Exception):
    pass
