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
        logger.debug(">>> Entering create()")
        import time; __log_start = time.time()
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        logger.debug("create(cls=%s): instance → %s", cls, instance)
        logger.debug("create(): instance → %s", instance)
        logger.info("create()=: save operation took %s ms", int((time.time() - __log_start) * 1000))
        logger.debug("<<< Exiting create()")
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        logger.debug(">>> Entering update(commit=%s)", commit)
        import time; __log_start = time.time()
        for attr, value in kwargs.items():
            setattr(self, attr, value)
            logger.debug("<<< Exiting update(commit=%s)", commit)
            logger.info("update(commit)=%s: save operation took %s ms", commit, int((time.time() - __log_start) * 1000))
        return commit and self.save() or self

    def save(self, commit=True):
        logger.debug(">>> Entering save(commit=%s)", commit)
        import time; __log_start = time.time()
        """Save the record."""
        logger.info("save(commit)=%s: save operation took %s ms", commit, int((time.time() - __log_start) * 1000))
        import time; __log_start = time.time()
        db.session.add(self)
        if commit:
            db.session.commit()
            logger.info("save(commit)=%s: database operation took %s ms", commit, int((time.time() - __log_start) * 1000))
            logger.debug("<<< Exiting save(commit=%s)", commit)
        return self

    def delete(self, commit=True):
        logger.debug(">>> Entering delete(commit=%s)", commit)
        import time; __log_start = time.time()
        """Remove the record from the database."""
        import time; __log_start = time.time()
        logger.info("delete(commit)=%s: delete operation took %s ms", commit, int((time.time() - __log_start) * 1000))
        logger.info("delete(commit)=%s: database operation took %s ms", commit, int((time.time() - __log_start) * 1000))
        db.session.delete(self)
        logger.debug("<<< Exiting delete(commit=%s)", commit)
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
