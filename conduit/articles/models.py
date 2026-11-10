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
        db.Model.__init__(self, tagname=tagname)
        logger.debug("<<< Exiting __init__(author=%s,title=%s,body=%s,description=%s,slug=%s)", author, title, body, description, slug, extra={"event.action": "__init__", "logrite.author": author, "logrite.title": title, "logrite.description": description, "logrite.slug": slug})

    def __repr__(self):
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
        logger.debug("__init__(author=%s,title=%s,body=%s,description=%s,slug=%s): slug → %s", author, title, body, description, slug, slug, extra={"event.action": "__init__", "logrite.author": author, "logrite.title": title, "logrite.description": description, "logrite.slug": slug})

    def favourite(self, profile):
        if not self.is_favourite(profile):
            self.favoriters.append(profile)
            return True
        logger.debug("<<< Exiting favourite(profile=%s)", profile, extra={"event.action": "favourite", "logrite.profile": profile})
        return False

    def unfavourite(self, profile):
        if self.is_favourite(profile):
            self.favoriters.remove(profile)
            return True
        logger.debug("<<< Exiting unfavourite(profile=%s)", profile, extra={"event.action": "unfavourite", "logrite.profile": profile})
        return False

    def is_favourite(self, profile):
        logger.info("is_favourite(profile)=%s: count operation executing", profile, extra={"event.action": "is_favourite", "event.category": "database", "logrite.profile": profile})
        logger.debug("<<< Exiting is_favourite(profile=%s)", profile, extra={"event.action": "is_favourite", "logrite.profile": profile})
        return bool(self.query.filter(favoriter_assoc.c.favoriter == profile.id).count())

    def add_tag(self, tag):
        if tag not in self.tagList:
            self.tagList.append(tag)
            return True
        logger.debug("<<< Exiting add_tag(tag=%s)", tag, extra={"event.action": "add_tag", "logrite.tag": tag})
        return False

    def remove_tag(self, tag):
        if tag in self.tagList:
            self.tagList.remove(tag)
            return True
        logger.debug("<<< Exiting remove_tag(tag=%s)", tag, extra={"event.action": "remove_tag", "logrite.tag": tag})
        return False

    @property
    def favoritesCount(self):
        logger.debug("<<< Exiting favoritesCount()", extra={"event.action": "favoritesCount"})
        return len(self.favoriters.all())

    @property
    def favorited(self):
        if current_user:
            logger.info("favorited()=: count operation executing", extra={"event.action": "favorited", "event.category": "database"})
            profile = current_user.profile
            logger.debug("favorited(self=%s): profile → %s", self, profile, extra={"event.action": "favorited"})
            return self.query.join(Article.favoriters).filter(UserProfile.id == profile.id).count() == 1
        return False
