from marshmallow import Schema, fields, pre_load, post_dump
import logging
logger = logging.getLogger(__name__)


class ProfileSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    bio = fields.Str()
    image = fields.Url()
    following = fields.Boolean()
    # ugly hack.
    profile = fields.Nested('self', exclude=('profile',), default=True, load_only=True)

    @pre_load
    def make_user(self, data, **kwargs):
        logger.debug("<<< Exiting make_user(data=%s)", data, extra={"event.action": "make_user"})
        return data['profile']

    @post_dump
    def dump_user(self, data, **kwargs):
        logger.debug("<<< Exiting dump_user(data=%s)", data, extra={"event.action": "dump_user"})
        return {'profile': data}

    class Meta:
        strict = True


profile_schema = ProfileSchema()
profile_schemas = ProfileSchema(many=True)
