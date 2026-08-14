from flask import jsonify
import logging
logger = logging.getLogger(__name__)


def template(data, code=500):
    logger.debug(">>> Entering template(data=%s,code=%s)", data, code)
    logger.debug("<<< Exiting template(data=%s,code=%s)", data, code)
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = template(['User not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
UNKNOWN_ERROR = template([], code=500)
ARTICLE_NOT_FOUND = template(['Article not found'], code=404)
COMMENT_NOT_OWNED = template(['Not your article'], code=422)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        logger.debug(">>> Entering __init__(message=%s,status_code=%s,payload=%s)", message, status_code, payload)
        Exception.__init__(self)
        self.message = message
        logger.debug("__init__(self=%s,message=%s,status_code=%s,payload=%s): self.message → %s", self, message, status_code, payload, self.message)
        logger.debug("__init__(self=%s,message=%s,status_code=%s,payload=%s): self.status_code → %s", self, message, status_code, payload, self.status_code)
        logger.debug("__init__(self=%s,message=%s,status_code=%s,payload=%s): self.payload → %s", self, message, status_code, payload, self.payload)
        if status_code is not None:
            logger.debug("<<< Exiting __init__(message=%s,status_code=%s,payload=%s)", message, status_code, payload)
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        logger.debug(">>> Entering to_json()")
        rv = self.message
        logger.debug("<<< Exiting to_json()")
        return jsonify(rv)

    @classmethod
    def user_not_found(cls):
        logger.debug(">>> Entering user_not_found()")
        logger.debug("<<< Exiting user_not_found()")
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        logger.debug(">>> Entering user_already_registered()")
        logger.debug("<<< Exiting user_already_registered()")
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls):
        logger.debug(">>> Entering unknown_error()")
        logger.debug("<<< Exiting unknown_error()")
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def article_not_found(cls):
        logger.debug(">>> Entering article_not_found()")
        logger.debug("<<< Exiting article_not_found()")
        return cls(**ARTICLE_NOT_FOUND)

    @classmethod
    def comment_not_owned(cls):
        logger.debug(">>> Entering comment_not_owned()")
        logger.debug("<<< Exiting comment_not_owned()")
        return cls(**COMMENT_NOT_OWNED)
