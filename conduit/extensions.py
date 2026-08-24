# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
import logging


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        logger.debug(">>> Entering create()")
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

        logger.debug("create(cls=%s): instance → %s", cls, instance)
    def update(self, commit=True, **kwargs):
        logger.debug(">>> Entering update(commit=%s)", commit)
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        logger.debug("<<< Exiting update(commit=%s)", commit)
        return commit and self.save() or self

    def save(self, commit=True):
        logger.debug(">>> Entering save(commit=%s)", commit)
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
        logger.info("save(commit)=%s: database operation took %s ms", commit, int((time.time() - start_time) * 1000))
        logger.debug("<<< Exiting save(commit=%s)", commit)

    def delete(self, commit=True):
        logger.debug(">>> Entering delete(commit=%s)", commit)
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

        import time
start_time = time.time()
logger.info("delete(commit)=%s: delete operation took %s ms", commit, int((time.time() - start_time) * 1000))
logger.info("delete(commit)=%s: database operation took %s ms", commit, int((time.time() - start_time) * 1000))

bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()
cache = Cache()
cors = CORS()

from conduit.utils import jwt_identity, identity_loader  # noqa

jwt = JWTManager()
jwt.user_loader_callback_loader(jwt_identity)
jwt.user_identity_loader(identity_loader)
