# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump

from conduit.profile.serializers import ProfileSchema
import logging
logger = logging.getLogger(__name__)


class TagSchema(Schema):
    tagname = fields.Str()


class ArticleSchema(Schema):
    slug = fields.Str()
    title = fields.Str()
    description = fields.Str()
    createdAt = fields.DateTime()
    body = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)
    tagList = fields.List(fields.Str())
    favoritesCount = fields.Int(dump_only=True)
    favorited = fields.Bool(dump_only=True)

    @pre_load
    def make_article(self, data, **kwargs):
        logger.info("CUSTOM-AUDIT[070ab3]: ENTERING: make_article() method", extra={"event.action": "make_article"})
        logger.debug("<<< Exiting make_article(data=%s)", data, extra={"event.action": "make_article"})
        return data['article']

    @post_dump
    def dump_article(self, data, **kwargs):
        data['author'] = data['author']['profile']
        logger.debug("<<< Exiting dump_article(data=%s)", data, extra={"event.action": "dump_article"})
        return {'article': data}

    class Meta:
        strict = True


class ArticleSchemas(ArticleSchema):

    @post_dump
    def dump_article(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def dump_articles(self, data, many, **kwargs):
        logger.debug("<<< Exiting dump_articles(data=%s,many=%s)", data, many, extra={"event.action": "dump_articles", "logrite.many": many})
        return {'articles': data, 'articlesCount': len(data)}


class CommentSchema(Schema):
    createdAt = fields.DateTime()
    body = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    id = fields.Int()

    # for the envelope
    comment = fields.Nested('self', exclude=('comment',), default=True, load_only=True)

    @pre_load
    def make_comment(self, data, **kwargs):
        logger.debug("<<< Exiting make_comment(data=%s)", data, extra={"event.action": "make_comment"})
        return data['comment']

    @post_dump
    def dump_comment(self, data, **kwargs):
        data['author'] = data['author']['profile']
        logger.debug("<<< Exiting dump_comment(data=%s)", data, extra={"event.action": "dump_comment"})
        return {'comment': data}

    class Meta:
        strict = True


class CommentsSchema(CommentSchema):

    @post_dump
    def dump_comment(self, data, **kwargs):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def make_comment(self, data, many, **kwargs):
        logger.debug("<<< Exiting make_comment(data=%s,many=%s)", data, many, extra={"event.action": "make_comment", "logrite.many": many})
        return {'comments': data}


article_schema = ArticleSchema()
articles_schema = ArticleSchemas(many=True)
comment_schema = CommentSchema()
comments_schema = CommentsSchema(many=True)
