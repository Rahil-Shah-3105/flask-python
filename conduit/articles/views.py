# coding: utf-8

import datetime as dt

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required, jwt_optional
from marshmallow import fields

from conduit.exceptions import InvalidUsage
from conduit.user.models import User
from .models import Article, Tags, Comment
from .serializers import (article_schema, articles_schema, comment_schema,
                          comments_schema)
import time
import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('articles', __name__)


##########
# Articles
##########

@blueprint.route('/api/articles', methods=('GET',))
@jwt_optional
@use_kwargs({'tag': fields.Str(), 'author': fields.Str(),
             'favorited': fields.Str(), 'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def get_articles(tag=None, author=None, favorited=None, limit=20, offset=0):
    logger.error(">>> Entering get_articles(tag=%s,author=%s,favorited=%s,limit=%s,offset=%s)", tag, author, favorited, limit, offset, extra={"event.action": "get_articles", "logrite.tag": tag, "logrite.author": author, "logrite.favorited": favorited, "logrite.limit": limit, "logrite.offset": offset})
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.tagname == tag))
        logger.error("get_articles(tag=%s,author=%s,favorited=%s,limit=%s,offset=%s): res → %s", tag, author, favorited, limit, offset, res, extra={"event.action": "get_articles", "logrite.tag": tag, "logrite.author": author, "logrite.favorited": favorited, "logrite.limit": limit, "logrite.offset": offset})
    if author:
        res = res.join(Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    logger.warning("<<< Exiting get_articles(tag=%s,author=%s,favorited=%s,limit=%s,offset=%s)", tag, author, favorited, limit, offset, extra={"event.action": "get_articles", "logrite.tag": tag, "logrite.author": author, "logrite.favorited": favorited, "logrite.limit": limit, "logrite.offset": offset})
    return res.offset(offset).limit(limit).all()


@blueprint.route('/api/articles', methods=('POST',))
@jwt_required
@use_kwargs(article_schema)
@marshal_with(article_schema)
def make_article(body, title, description, tagList=None):
    logger.error(">>> Entering make_article(body=%s,title=%s,description=%s,tagList=%s)", body, title, description, tagList, extra={"event.action": "make_article", "logrite.title": title, "logrite.description": description, "logrite.tagList": tagList})
    article = Article(title=title, description=description, body=body,
                      author=current_user.profile)
    if tagList is not None:
        for tag in tagList:
            mtag = Tags.query.filter_by(tagname=tag).first()
            logger.error("make_article(body=%s,title=%s,description=%s,tagList=%s): mtag → %s", body, title, description, tagList, mtag, extra={"event.action": "make_article", "logrite.title": title, "logrite.description": description, "logrite.tagList": tagList})
            if not mtag:
                mtag = Tags(tag)
                mtag.save()
            article.add_tag(mtag)
    article.save()
    logger.warning("<<< Exiting make_article(body=%s,title=%s,description=%s,tagList=%s)", body, title, description, tagList, extra={"event.action": "make_article", "logrite.title": title, "logrite.description": description, "logrite.tagList": tagList})
    return article


@blueprint.route('/api/articles/<slug>', methods=('PUT',))
@jwt_required
@use_kwargs(article_schema)
@marshal_with(article_schema)
def update_article(slug, **kwargs):
    logger.error(">>> Entering update_article(slug=%s)", slug, extra={"event.action": "update_article", "logrite.slug": slug})
    __log_start = time.time()
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    logger.error("update_article(slug=%s): article → %s", slug, article, extra={"event.action": "update_article", "logrite.slug": slug})
    if not article:
        raise InvalidUsage.article_not_found()
    article.update(updatedAt=dt.datetime.utcnow(), **kwargs)
    logger.error("update_article(slug)=%s: query operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "update_article", "event.category": "database", "logrite.slug": slug})
    logger.error("update_article(slug)=%s: save operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "update_article", "event.category": "database", "logrite.slug": slug})
    article.save()
    logger.error("update_article(slug)=%s: update operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "update_article", "event.category": "database", "logrite.slug": slug})
    logger.warning("<<< Exiting update_article(slug=%s)", slug, extra={"event.action": "update_article", "logrite.slug": slug})
    return article


@blueprint.route('/api/articles/<slug>', methods=('DELETE',))
@jwt_required
def delete_article(slug):
    logger.error(">>> Entering delete_article(slug=%s)", slug, extra={"event.action": "delete_article", "logrite.slug": slug})
    __log_start = time.time()
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    logger.error("delete_article(slug=%s): article → %s", slug, article, extra={"event.action": "delete_article", "logrite.slug": slug})
    logger.error("delete_article(slug)=%s: delete operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "delete_article", "event.category": "database", "logrite.slug": slug})
    article.delete()
    logger.error("delete_article(slug)=%s: query operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "delete_article", "event.category": "database", "logrite.slug": slug})
    logger.warning("<<< Exiting delete_article(slug=%s)", slug, extra={"event.action": "delete_article", "logrite.slug": slug})
    return '', 200


@blueprint.route('/api/articles/<slug>', methods=('GET',))
@jwt_optional
@marshal_with(article_schema)
def get_article(slug):
    logger.error(">>> Entering get_article(slug=%s)", slug, extra={"event.action": "get_article", "logrite.slug": slug})
    __log_start = time.time()
    article = Article.query.filter_by(slug=slug).first()
    logger.error("get_article(slug)=%s: query operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "get_article", "event.category": "database", "logrite.slug": slug})
    logger.error("get_article(slug=%s): article → %s", slug, article, extra={"event.action": "get_article", "logrite.slug": slug})
    if not article:
        raise InvalidUsage.article_not_found()
    logger.warning("<<< Exiting get_article(slug=%s)", slug, extra={"event.action": "get_article", "logrite.slug": slug})
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('POST',))
@jwt_required
@marshal_with(article_schema)
def favorite_an_article(slug):
    logger.error(">>> Entering favorite_an_article(slug=%s)", slug, extra={"event.action": "favorite_an_article", "logrite.slug": slug})
    __log_start = time.time()
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    logger.error("favorite_an_article(slug=%s): article → %s", slug, article, extra={"event.action": "favorite_an_article", "logrite.slug": slug})
    if not article:
        raise InvalidUsage.article_not_found()
    article.favourite(profile)
    logger.error("favorite_an_article(slug)=%s: query operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "favorite_an_article", "event.category": "database", "logrite.slug": slug})
    article.save()
    logger.error("favorite_an_article(slug)=%s: save operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "favorite_an_article", "event.category": "database", "logrite.slug": slug})
    logger.warning("<<< Exiting favorite_an_article(slug=%s)", slug, extra={"event.action": "favorite_an_article", "logrite.slug": slug})
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('DELETE',))
@jwt_required
@marshal_with(article_schema)
def unfavorite_an_article(slug):
    logger.error(">>> Entering unfavorite_an_article(slug=%s)", slug, extra={"event.action": "unfavorite_an_article", "logrite.slug": slug})
    __log_start = time.time()
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    logger.error("unfavorite_an_article(slug=%s): article → %s", slug, article, extra={"event.action": "unfavorite_an_article", "logrite.slug": slug})
    if not article:
        raise InvalidUsage.article_not_found()
    article.unfavourite(profile)
    logger.error("unfavorite_an_article(slug)=%s: query operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "unfavorite_an_article", "event.category": "database", "logrite.slug": slug})
    article.save()
    logger.error("unfavorite_an_article(slug)=%s: save operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "unfavorite_an_article", "event.category": "database", "logrite.slug": slug})
    logger.warning("<<< Exiting unfavorite_an_article(slug=%s)", slug, extra={"event.action": "unfavorite_an_article", "logrite.slug": slug})
    return article


@blueprint.route('/api/articles/feed', methods=('GET',))
@jwt_required
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def articles_feed(limit=20, offset=0):
    logger.error(">>> Entering articles_feed(limit=%s,offset=%s)", limit, offset, extra={"event.action": "articles_feed", "logrite.limit": limit, "logrite.offset": offset})
    return Article.query.join(current_user.profile.follows). \
        order_by(Article.createdAt.desc()).offset(offset).limit(limit).all()
    logger.warning("<<< Exiting articles_feed(limit=%s,offset=%s)", limit, offset, extra={"event.action": "articles_feed", "logrite.limit": limit, "logrite.offset": offset})


######
# Tags
######

@blueprint.route('/api/tags', methods=('GET',))
def get_tags():
    logger.error(">>> Entering get_tags()", extra={"event.action": "get_tags"})
    logger.warning("<<< Exiting get_tags()", extra={"event.action": "get_tags"})
    return jsonify({'tags': [tag.tagname for tag in Tags.query.all()]})


##########
# Comments
##########


@blueprint.route('/api/articles/<slug>/comments', methods=('GET',))
@marshal_with(comments_schema)
def get_comments(slug):
    logger.error(">>> Entering get_comments(slug=%s)", slug, extra={"event.action": "get_comments", "logrite.slug": slug})
    __log_start = time.time()
    article = Article.query.filter_by(slug=slug).first()
    logger.error("get_comments(slug)=%s: query operation took %s ms", slug, int((time.time() - __log_start) * 1000), extra={"event.action": "get_comments", "event.category": "database", "logrite.slug": slug})
    logger.error("get_comments(slug=%s): article → %s", slug, article, extra={"event.action": "get_comments", "logrite.slug": slug})
    if not article:
        raise InvalidUsage.article_not_found()
    logger.warning("<<< Exiting get_comments(slug=%s)", slug, extra={"event.action": "get_comments", "logrite.slug": slug})
    return article.comments


@blueprint.route('/api/articles/<slug>/comments', methods=('POST',))
@jwt_required
@use_kwargs(comment_schema)
@marshal_with(comment_schema)
def make_comment_on_article(slug, body, **kwargs):
    logger.error(">>> Entering make_comment_on_article(slug=%s,body=%s)", slug, body, extra={"event.action": "make_comment_on_article", "logrite.slug": slug})
    __log_start = time.time()
    article = Article.query.filter_by(slug=slug).first()
    logger.error("make_comment_on_article(slug,body)=%s,%s: query operation took %s ms", slug, body, int((time.time() - __log_start) * 1000), extra={"event.action": "make_comment_on_article", "event.category": "database", "logrite.slug": slug})
    logger.error("make_comment_on_article(slug=%s,body=%s): article → %s", slug, body, article, extra={"event.action": "make_comment_on_article", "logrite.slug": slug})
    if not article:
        raise InvalidUsage.article_not_found()
    comment = Comment(article, current_user.profile, body, **kwargs)
    logger.error("make_comment_on_article(slug=%s,body=%s): comment → %s", slug, body, comment, extra={"event.action": "make_comment_on_article", "logrite.slug": slug})
    comment.save()
    logger.error("make_comment_on_article(slug,body)=%s,%s: save operation took %s ms", slug, body, int((time.time() - __log_start) * 1000), extra={"event.action": "make_comment_on_article", "event.category": "database", "logrite.slug": slug})
    logger.warning("<<< Exiting make_comment_on_article(slug=%s,body=%s)", slug, body, extra={"event.action": "make_comment_on_article", "logrite.slug": slug})
    return comment


@blueprint.route('/api/articles/<slug>/comments/<cid>', methods=('DELETE',))
@jwt_required
def delete_comment_on_article(slug, cid):
    logger.error(">>> Entering delete_comment_on_article(slug=%s,cid=%s)", slug, cid, extra={"event.action": "delete_comment_on_article", "logrite.slug": slug, "logrite.cid": cid})
    __log_start = time.time()
    article = Article.query.filter_by(slug=slug).first()
    logger.error("delete_comment_on_article(slug,cid)=%s,%s: query operation took %s ms", slug, cid, int((time.time() - __log_start) * 1000), extra={"event.action": "delete_comment_on_article", "event.category": "database", "logrite.slug": slug, "logrite.cid": cid})
    logger.error("delete_comment_on_article(slug=%s,cid=%s): article → %s", slug, cid, article, extra={"event.action": "delete_comment_on_article", "logrite.slug": slug, "logrite.cid": cid})
    if not article:
        raise InvalidUsage.article_not_found()

    comment = article.comments.filter_by(id=cid, author=current_user.profile).first()
    logger.error("delete_comment_on_article(slug=%s,cid=%s): comment → %s", slug, cid, comment, extra={"event.action": "delete_comment_on_article", "logrite.slug": slug, "logrite.cid": cid})
    comment.delete()
    logger.error("delete_comment_on_article(slug,cid)=%s,%s: delete operation took %s ms", slug, cid, int((time.time() - __log_start) * 1000), extra={"event.action": "delete_comment_on_article", "event.category": "database", "logrite.slug": slug, "logrite.cid": cid})
    logger.warning("<<< Exiting delete_comment_on_article(slug=%s,cid=%s)", slug, cid, extra={"event.action": "delete_comment_on_article", "logrite.slug": slug, "logrite.cid": cid})
    return '', 200
