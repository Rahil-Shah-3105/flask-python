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
import time
import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('user', __name__)


@blueprint.route('/api/users', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username, password, email, **kwargs):
    logger.error(">>> Entering register_user(username=%s,password=<redacted>,email=<redacted>)", username, extra={"event.action": "register_user", "user.name": str(username)})
    __log_start = time.time()
    try:
        userprofile = UserProfile(User(username, email, password=password, **kwargs).save()).save()
        logger.error("register_user(username=%s,password=<redacted>,email=<redacted>): userprofile → %s", username, userprofile, extra={"event.action": "register_user", "user.name": str(username)})
        userprofile.user.token = create_access_token(identity=userprofile.user)
    except IntegrityError:
        logger.error("Exception in register_user(username=%s,password=<redacted>,email=<redacted>)", username, exc_info=True, extra={"event.action": "register_user", "event.category": "process", "user.name": str(username)})
        logger.error("register_user(username,password,email)=%s,<redacted>,<redacted>: database operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "register_user", "event.category": "database", "user.name": str(username)})
        db.session.rollback()
        logger.error("register_user(username,password,email)=%s,<redacted>,<redacted>: save operation took %s ms", username, int((time.time() - __log_start) * 1000), extra={"event.action": "register_user", "event.category": "database", "user.name": str(username)})
        raise InvalidUsage.user_already_registered()
    logger.warning("<<< Exiting register_user(username=%s,password=<redacted>,email=<redacted>)", username, extra={"event.action": "register_user", "user.name": str(username)})
    return userprofile.user


@blueprint.route('/api/users/login', methods=('POST',))
@jwt_optional
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    logger.error(">>> Entering login_user(email=<redacted>,password=<redacted>)", extra={"event.action": "login_user"})
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        logger.error("login_user(email=<redacted>,password=<redacted>): user → %s", user, extra={"event.action": "login_user"})
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        logger.warning("<<< Exiting login_user(email=<redacted>,password=<redacted>)", extra={"event.action": "login_user"})
        raise InvalidUsage.user_not_found()


@blueprint.route('/api/user', methods=('GET',))
@jwt_required
@marshal_with(user_schema)
def get_user():
    logger.error(">>> Entering get_user()", extra={"event.action": "get_user"})
    user = current_user
    # Not sure about this
    user.token = request.headers.environ['HTTP_AUTHORIZATION'].split('Token ')[1]
    logger.warning("<<< Exiting get_user()", extra={"event.action": "get_user"})
    return current_user


@blueprint.route('/api/user', methods=('PUT',))
@jwt_required
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    logger.error(">>> Entering update_user()", extra={"event.action": "update_user"})
    user = current_user
    logger.error("update_user(): user → %s", user, extra={"event.action": "update_user"})
    # take in consideration the password
    password = kwargs.pop('password', None)
    logger.error("update_user(): password → <redacted>", extra={"event.action": "update_user"})
    if password:
        user.set_password(password)
        logger.debug("update_user(): user → %s", user, extra={"event.action": "update_user"})
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    logger.warning("<<< Exiting update_user()", extra={"event.action": "update_user"})
    return user
