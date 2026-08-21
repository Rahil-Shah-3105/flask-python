# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt_extended import current_user, jwt_required, jwt_optional

from conduit.exceptions import InvalidUsage
from conduit.user.models import User
from .serializers import profile_schema
import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('profiles', __name__)


@blueprint.route('/api/profiles/<username>', methods=('GET',))
@jwt_optional
@marshal_with(profile_schema)
def get_profile(username):
    logger.debug(">>> Entering get_profile(username=%s)", username)
    import time; __log_start = time.time()
    user = User.query.filter_by(username=username).first()
    logger.debug("get_profile(username=%s): user → %s", username, user)
    if not user:
        raise InvalidUsage.user_not_found()
        logger.info("get_profile(username)=%s: query operation took %s ms", username, int((time.time() - __log_start) * 1000))
    logger.debug("<<< Exiting get_profile(username=%s)", username)
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=('POST',))
@jwt_required
@marshal_with(profile_schema)
def follow_user(username):
    logger.debug(">>> Entering follow_user(username=%s)", username)
    import time; __log_start = time.time()
    user = User.query.filter_by(username=username).first()
    logger.debug("follow_user(username=%s): user → %s", username, user)
    if not user:
        raise InvalidUsage.user_not_found()
        logger.info("follow_user(username)=%s: query operation took %s ms", username, int((time.time() - __log_start) * 1000))
    current_user.profile.follow(user.profile)
    current_user.profile.save()
    logger.info("follow_user(username)=%s: save operation took %s ms", username, int((time.time() - __log_start) * 1000))
    logger.debug("<<< Exiting follow_user(username=%s)", username)
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=('DELETE',))
@jwt_required
@marshal_with(profile_schema)
def unfollow_user(username):
    logger.debug(">>> Entering unfollow_user(username=%s)", username)
    import time; __log_start = time.time()
    user = User.query.filter_by(username=username).first()
    logger.debug("unfollow_user(username=%s): user → %s", username, user)
    if not user:
        raise InvalidUsage.user_not_found()
        logger.info("unfollow_user(username)=%s: query operation took %s ms", username, int((time.time() - __log_start) * 1000))
    current_user.profile.unfollow(user.profile)
    current_user.profile.save()
    logger.info("unfollow_user(username)=%s: save operation took %s ms", username, int((time.time() - __log_start) * 1000))
    logger.debug("<<< Exiting unfollow_user(username=%s)", username)
    return user.profile
