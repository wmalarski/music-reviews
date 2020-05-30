from graphql_jwt.exceptions import PermissionDenied


def check_permissions(user, info):
    if info.context.user != user:
        raise PermissionDenied()
