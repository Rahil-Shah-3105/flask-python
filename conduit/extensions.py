# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
import logging
logger = logging.getLogger(__name__)


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        logger.info("create()=: save operation executing", extra={"event.action": "create", "event.category": "database"})
        instance = cls(**kwargs)
        logger.debug("create(cls=%s): instance → %s", cls, instance, extra={"event.action": "create"})
        logger.debug("create(): instance → %s", instance, extra={"event.action": "create"})
        logger.debug("<<< Exiting create()", extra={"event.action": "create"})
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        logger.info("update(commit)=%s: save operation executing", commit, extra={"event.action": "update", "event.category": "database", "logrite.commit": commit})
        logger.debug("<<< Exiting update(commit=%s)", commit, extra={"event.action": "update", "logrite.commit": commit})
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        __log_start = time.time()
        db.session.add(self)
        logger.info("save(commit)=%s: save operation took %s ms", commit, int((time.time() - __log_start) * 1000), extra={"event.action": "save", "event.category": "database", "logrite.commit": commit})
        if commit:
            db.session.commit()
        logger.info("save(commit)=%s: database operation took %s ms", commit, int((time.time() - __log_start) * 1000), extra={"event.action": "save", "event.category": "database", "logrite.commit": commit})
        logger.debug("<<< Exiting save(commit=%s)", commit, extra={"event.action": "save", "logrite.commit": commit})
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        logger.info("delete(commit)=%s: database operation executing", commit, extra={"event.action": "delete", "event.category": "database", "logrite.commit": commit})
        db.session.delete(self)
        logger.debug("<<< Exiting delete(commit=%s)", commit, extra={"event.action": "delete", "logrite.commit": commit})
        return commit and db.session.commit()


bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()
cache = Cache()
cors = CORS()

from conduit.utils import jwt_identity, identity_loader  # noqa

jwt = JWTManager()
jwt.user_loader_callback_loader(jwt_identity)
jwt.user_identity_loader(identity_loader)
