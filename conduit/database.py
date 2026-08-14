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
        logger.debug(">>> Entering get_by_id(record_id=%s)", record_id)
        import time; __log_start = time.time()
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            logger.debug("<<< Exiting get_by_id(record_id=%s)", record_id)
            logger.info("get_by_id(record_id)=%s: find operation took %s ms", record_id, int((time.time() - __log_start) * 1000))
            return cls.query.get(int(record_id))


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    logger.debug(">>> Entering reference_col(tablename=%s,nullable=%s,pk_name=%s)", tablename, nullable, pk_name)
    """Column that adds primary key foreign key reference.

    Usage: ::
        logger.debug("reference_col(tablename=%s,nullable=%s,pk_name=%s): category → %s", tablename, nullable, pk_name, category)

        category_id = reference_col('category')
        logger.debug("reference_col(tablename=%s,nullable=%s,pk_name=%s): category_id → %s", tablename, nullable, pk_name, category_id)
        category = relationship('Category', backref='categories')
    """
    logger.debug("<<< Exiting reference_col(tablename=%s,nullable=%s,pk_name=%s)", tablename, nullable, pk_name)
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)
