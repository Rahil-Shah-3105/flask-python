# coding: utf-8

import datetime as dt

from flask_jwt_extended import current_user
from slugify import slugify

from conduit.database import (Model, SurrogatePK, db, Column,
                              reference_col, relationship)
from conduit.profile.models import UserProfile
import logging
logger = logging.getLogger(__name__)

favoriter_assoc = db.Table("favoritor_assoc",
                           db.Column("favoriter", db.Integer, db.ForeignKey("userprofile.id")),
                           db.Column("favorited_article", db.Integer, db.ForeignKey("article.id")))

tag_assoc = db.Table("tag_assoc",
                     db.Column("tag", db.Integer, db.ForeignKey("tags.id")),
                     db.Column("article", db.Integer, db.ForeignKey("article.id")))


class Tags(Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(100))

    def __init__(self, tagname):
        logger.debug(">>> Entering __init__(tagname=%s)", tagname)
        db.Model.__init__(self, tagname=tagname)
        logger.debug("<<< Exiting __init__(tagname=%s)", tagname)
        logger.debug(">>> Entering __init__(article=%s,author=%s,body=%s)", article, author, body)
        logger.debug("<<< Exiting __init__(article=%s,author=%s,body=%s)", article, author, body)

    def __repr__(self):
        logger.debug(">>> Entering __repr__()")
        logger.debug("<<< Exiting __repr__()")
        return self.tagname


class Comment(Model, SurrogatePK):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    body = Column(db.Text)
    createdAt = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updatedAt = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    author_id = reference_col('userprofile', nullable=False)
    author = relationship('UserProfile', backref=db.backref('comments'))
    article_id = reference_col('article', nullable=False)

    def __init__(self, article, author, body, **kwargs):
        db.Model.__init__(self, author=author, body=body, article=article, **kwargs)

        logger.debug(">>> Entering __init__(author=%s,title=%s,body=%s,description=%s,slug=%s)", author, title, body, description, slug)
        logger.debug("__init__(author=%s,title=%s,body=%s,description=%s,slug=%s): slug → %s", author, title, body, description, slug, slug)

class Article(SurrogatePK, Model):
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    slug = Column(db.Text, unique=True)
    title = Column(db.String(100), nullable=False)
    description = Column(db.Text, nullable=False)
    body = Column(db.Text)
    createdAt = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updatedAt = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    author_id = reference_col('userprofile', nullable=False)
    author = relationship('UserProfile', backref=db.backref('articles'))
    favoriters = relationship(
        'UserProfile',
        secondary=favoriter_assoc,
        backref='favorites',
        lazy='dynamic')

    tagList = relationship(
        'Tags', secondary=tag_assoc, backref='articles')

    comments = relationship('Comment', backref=db.backref('article'), lazy='dynamic')

    def __init__(self, author, title, body, description, slug=None, **kwargs):
        db.Model.__init__(self, author=author, title=title, description=description, body=body,
                          slug=slug or slugify(title), **kwargs)
        logger.debug("<<< Exiting __init__(author=%s,title=%s,body=%s,description=%s,slug=%s)", author, title, body, description, slug)

    def favourite(self, profile):
        logger.debug(">>> Entering favourite(profile=%s)", profile)
        if not self.is_favourite(profile):
            self.favoriters.append(profile)
            return True
            logger.debug("<<< Exiting favourite(profile=%s)", profile)
        return False

    def unfavourite(self, profile):
        logger.debug(">>> Entering unfavourite(profile=%s)", profile)
        if self.is_favourite(profile):
            self.favoriters.remove(profile)
            return True
            logger.debug("<<< Exiting unfavourite(profile=%s)", profile)
        return False

    def is_favourite(self, profile):
        logger.debug(">>> Entering is_favourite(profile=%s)", profile)
        import time; __log_start = time.time()
        logger.info("is_favourite(profile)=%s: count operation took %s ms", profile, int((time.time() - __log_start) * 1000))
        logger.debug("<<< Exiting is_favourite(profile=%s)", profile)
        return bool(self.query.filter(favoriter_assoc.c.favoriter == profile.id).count())

    def add_tag(self, tag):
        logger.debug(">>> Entering add_tag(tag=%s)", tag)
        if tag not in self.tagList:
            self.tagList.append(tag)
            return True
            logger.debug("<<< Exiting add_tag(tag=%s)", tag)
        return False

    def remove_tag(self, tag):
        logger.debug(">>> Entering remove_tag(tag=%s)", tag)
        if tag in self.tagList:
            self.tagList.remove(tag)
            return True
            logger.debug("<<< Exiting remove_tag(tag=%s)", tag)
        return False

    @property
    def favoritesCount(self):
        logger.debug(">>> Entering favoritesCount()")
        logger.debug("<<< Exiting favoritesCount()")
        return len(self.favoriters.all())

    @property
    def favorited(self):
        logger.debug(">>> Entering favorited()")
        import time; __log_start = time.time()
        if current_user:
            profile = current_user.profile
            logger.debug("favorited(self=%s): profile → %s", self, profile)
            logger.info("favorited()=: count operation took %s ms", int((time.time() - __log_start) * 1000))
            return self.query.join(Article.favoriters).filter(UserProfile.id == profile.id).count() == 1
            logger.debug("<<< Exiting favorited()")
        return False
