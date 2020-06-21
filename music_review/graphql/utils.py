from typing import Any, Dict

from django.db import models
from graphql_jwt.exceptions import PermissionDenied


def check_permissions(user, info):
    if info.context.user != user:
        raise PermissionDenied()


def update_and_save(model: models.Model, kwargs: Dict[str, Any]):
    for key, value in kwargs.items():
        if value is not None or getattr(model.__class__, key).field.null:
            setattr(model, key, value)
    model.save()
