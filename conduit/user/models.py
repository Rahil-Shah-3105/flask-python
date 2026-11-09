# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from conduit.database import Column, Model, SurrogatePK, db
from conduit.extensions import bcrypt
import logging
logger = logging.getLogger(__name__)


class User(SurrogatePK, Model):

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    bio = Column(db.String(300), nullable=True)
    image = Column(db.String(120), nullable=True)
    token: str = ''

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            logger.debug("<<< Exiting __init__(username=%s,email=%s,password=<redacted>)", username, email, extra={"event.action": "__init__", "user.name": str(username)})
            self.password = None
            logger.debug("__init__(self=%s,username=%s,email=%s,password=<redacted>): self.password → <redacted>", self, username, email, extra={"event.action": "__init__", "user.name": str(username)})

    def set_password(self, password):
        """Set password."""
        logger.debug("<<< Exiting set_password(password=<redacted>)", extra={"event.action": "set_password"})
        logger.warning("set_password(password=<redacted>): self.password → <redacted>", extra={"event.action": "set_password"})
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        logger.debug("<<< Exiting check_password(value=%s)", value, extra={"event.action": "check_password", "logrite.value": value})
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        logger.debug("<<< Exiting __repr__()", extra={"event.action": "__repr__"})
        return '<User({username!r})>'.format(username=self.username)
