# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, create_access_token, current_user
from sqlalchemy.exc import IntegrityError

from conduit.database import db
from conduit.exceptions import InvalidUsage
from conduit.profile.models import UserProfile
from .models import User
from .serializers import user_schema
import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('user', __name__)


@blueprint.route('/api/users', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username, password, email, **kwargs):
    logger.debug(">>> Entering register_user(username=%s,password=<redacted>,email=%s)", username, email)
    import time; __log_start = time.time()
    try:
        userprofile = UserProfile(User(username, email, password=password, **kwargs).save()).save()
        logger.debug("register_user(username=%s,password=<redacted>,email=%s): userprofile → %s", username, email, userprofile)
        userprofile.user.token = create_access_token(identity=userprofile.user)
    except IntegrityError:
        logger.info("register_user(username,password,email)=%s,<redacted>,%s: save operation took %s ms", username, email, int((time.time() - __log_start) * 1000))
        db.session.rollback()
        logger.error("Exception in register_user(username=%s,password=<redacted>,email=%s)", username, email, exc_info=True)
        logger.info("register_user(username,password,email)=%s,<redacted>,%s: database operation took %s ms", username, email, int((time.time() - __log_start) * 1000))
        raise InvalidUsage.user_already_registered()
    logger.debug("<<< Exiting register_user(username=%s,password=<redacted>,email=%s)", username, email)
    return userprofile.user


@blueprint.route('/api/users/login', methods=('POST',))
@jwt_optional
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    logger.debug(">>> Entering login_user(email=%s,password=<redacted>)", email)
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        logger.debug("login_user(email=%s,password=<redacted>): user → %s", email, user)
        user.token = create_access_token(identity=user, fresh=True)
        logger.info("login_user(email,password)=%s,<redacted>: query operation took %s ms", email, int((time.time() - __log_start) * 1000))
        return user
    else:
        logger.debug("<<< Exiting login_user(email=%s,password=<redacted>)", email)
        raise InvalidUsage.user_not_found()


@blueprint.route('/api/user', methods=('GET',))
@jwt_required
@marshal_with(user_schema)
def get_user():
    logger.debug(">>> Entering get_user()")
    user = current_user
    logger.debug("get_user(): user → %s", user)
    # Not sure about this
    user.token = request.headers.environ['HTTP_AUTHORIZATION'].split('Token ')[1]
    logger.debug("<<< Exiting get_user()")
    return current_user


@blueprint.route('/api/user', methods=('PUT',))
@jwt_required
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    logger.debug(">>> Entering update_user()")
    user = current_user
    logger.debug("update_user(): user → %s", user)
    # take in consideration the password
    password = kwargs.pop('password', None)
    logger.warning("update_user(): password → %s", password)
    logger.debug("update_user(): password → <redacted>")
    if password:
        user.set_password(password)
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    logger.info("update_user()=: update operation took %s ms", int((time.time() - __log_start) * 1000))
    logger.debug("<<< Exiting update_user()")
    return user
