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
        logger.error(">>> Entering __init__(username=%s,email=<redacted>,password=<redacted>)", username, extra={"event.action": "__init__", "user.name": str(username)})
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            logger.warning("<<< Exiting __init__(username=%s,email=<redacted>,password=<redacted>)", username, extra={"event.action": "__init__", "user.name": str(username)})
            self.password = None
            logger.debug("__init__(self=%s,username=%s,email=<redacted>,password=<redacted>): self.password → <redacted>", self, username, extra={"event.action": "__init__", "user.name": str(username)})

    def set_password(self, password):
        """Set password."""
        logger.error(">>> Entering set_password(password=<redacted>)", extra={"event.action": "set_password"})
        self.password = bcrypt.generate_password_hash(password)
        logger.warning("<<< Exiting set_password(password=<redacted>)", extra={"event.action": "set_password"})
        logger.error("set_password(password=<redacted>): self.password → <redacted>", extra={"event.action": "set_password"})

    def check_password(self, value):
        """Check password."""
        logger.error(">>> Entering check_password(value=<redacted>)", extra={"event.action": "check_password"})
        logger.warning("<<< Exiting check_password(value=<redacted>)", extra={"event.action": "check_password"})
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        """Represent instance as a unique string."""
        logger.error(">>> Entering __repr__()", extra={"event.action": "__repr__"})
        logger.warning("<<< Exiting __repr__()", extra={"event.action": "__repr__"})
        return '<User({username!r})>'.format(username=self.username)
