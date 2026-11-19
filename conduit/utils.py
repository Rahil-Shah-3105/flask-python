# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from conduit.user.models import User  # noqa
import logging
logger = logging.getLogger(__name__)


def jwt_identity(payload):
    logger.error(">>> Entering jwt_identity(payload=%s)", payload, extra={"event.action": "jwt_identity"})
    logger.warning("<<< Exiting jwt_identity(payload=%s)", payload, extra={"event.action": "jwt_identity"})
    return User.get_by_id(payload)


def identity_loader(user):
    logger.error(">>> Entering identity_loader(user=%s)", user, extra={"event.action": "identity_loader", "user.name": str(user)})
    logger.warning("<<< Exiting identity_loader(user=%s)", user, extra={"event.action": "identity_loader", "user.name": str(user)})
    return user.id
