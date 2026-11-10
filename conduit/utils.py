# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from conduit.user.models import User  # noqa
import logging
logger = logging.getLogger(__name__)


def jwt_identity(payload):
    logger.debug("<<< Exiting jwt_identity(payload=%s)", payload, extra={"event.action": "jwt_identity"})
    return User.get_by_id(payload)


def identity_loader(user):
    return user.id
