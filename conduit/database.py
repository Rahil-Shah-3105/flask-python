# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from sqlalchemy.orm import relationship

from .compat import basestring
from .extensions import db
import logging
logger = logging.getLogger(__name__)

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship
Model = db.Model

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            logger.info("get_by_id(record_id)=%s: find operation executing", record_id, extra={"event.action": "get_by_id", "event.category": "database", "logrite.record_id": record_id})
            logger.debug("<<< Exiting get_by_id(record_id=%s)", record_id, extra={"event.action": "get_by_id", "logrite.record_id": record_id})
            return cls.query.get(int(record_id))


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    logger.debug("reference_col(tablename=%s,nullable=%s,pk_name=%s): category → %s", tablename, nullable, pk_name, category, extra={"event.action": "reference_col", "logrite.tablename": tablename, "logrite.nullable": nullable, "logrite.pk_name": pk_name})
    logger.debug("reference_col(tablename=%s,nullable=%s,pk_name=%s): category_id → %s", tablename, nullable, pk_name, category_id, extra={"event.action": "reference_col", "logrite.tablename": tablename, "logrite.nullable": nullable, "logrite.pk_name": pk_name})
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
