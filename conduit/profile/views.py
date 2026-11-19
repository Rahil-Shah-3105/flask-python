# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt_extended import current_user, jwt_required, jwt_optional

from conduit.exceptions import InvalidUsage
from conduit.user.models import User
from .serializers import profile_schema
import time
import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('profiles', __name__)


@blueprint.route('/api/profiles/<username>', methods=('GET',))
@jwt_optional
@marshal_with(profile_schema)
def get_profile(username):
    logger.error(">>> Entering get_profile(username=%s)", username, extra={"event.action": "get_profile", "user.name": str(username)})
    __log_start = time.time()
    user = User.query.filter_by(username=username).first()
    logger.error("get_profile(username=%s): user → %s", username, user, extra={"event.action": "get_profile", "user.name": str(username)})
    if not user:
        logger.error("get_profile(username)=%s: query operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "get_profile", "event.category": "database", "user.name": str(username)})
        raise InvalidUsage.user_not_found()
    logger.warning("<<< Exiting get_profile(username=%s)", username, extra={"event.action": "get_profile", "user.name": str(username)})
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=('POST',))
@jwt_required
@marshal_with(profile_schema)
def follow_user(username):
    logger.error(">>> Entering follow_user(username=%s)", username, extra={"event.action": "follow_user", "user.name": str(username)})
    __log_start = time.time()
    user = User.query.filter_by(username=username).first()
    logger.error("follow_user(username=%s): user → %s", username, user, extra={"event.action": "follow_user", "user.name": str(username)})
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.follow(user.profile)
    logger.error("follow_user(username)=%s: query operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "follow_user", "event.category": "database", "user.name": str(username)})
    current_user.profile.save()
    logger.error("follow_user(username)=%s: save operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "follow_user", "event.category": "database", "user.name": str(username)})
    logger.warning("<<< Exiting follow_user(username=%s)", username, extra={"event.action": "follow_user", "user.name": str(username)})
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=('DELETE',))
@jwt_required
@marshal_with(profile_schema)
def unfollow_user(username):
    logger.error(">>> Entering unfollow_user(username=%s)", username, extra={"event.action": "unfollow_user", "user.name": str(username)})
    __log_start = time.time()
    user = User.query.filter_by(username=username).first()
    logger.error("unfollow_user(username=%s): user → %s", username, user, extra={"event.action": "unfollow_user", "user.name": str(username)})
    if not user:
        raise InvalidUsage.user_not_found()
    current_user.profile.unfollow(user.profile)
    logger.error("unfollow_user(username)=%s: query operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "unfollow_user", "event.category": "database", "user.name": str(username)})
    current_user.profile.save()
    logger.error("unfollow_user(username)=%s: save operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "unfollow_user", "event.category": "database", "user.name": str(username)})
    logger.warning("<<< Exiting unfollow_user(username=%s)", username, extra={"event.action": "unfollow_user", "user.name": str(username)})
    return user.profile
