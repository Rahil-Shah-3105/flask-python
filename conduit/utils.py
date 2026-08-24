# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from conduit.user.models import User  # noqa
import logging


def jwt_identity(payload):
    logger.debug(">>> Entering jwt_identity(payload=%s)", payload)
    logger.debug("<<< Exiting jwt_identity(payload=%s)", payload)
    return User.get_by_id(payload)


def identity_loader(user):
    logger.debug(">>> Entering identity_loader(user=%s)", user)
    return user.id
