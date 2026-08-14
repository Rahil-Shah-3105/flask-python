# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask
from conduit.extensions import bcrypt, cache, db, migrate, jwt, cors

from conduit import commands, user, profile, articles, reports
from conduit.settings import ProdConfig
from conduit.exceptions import InvalidUsage
import logging
logger = logging.getLogger(__name__)


def create_app(config_object=ProdConfig):
    logger.debug(">>> Entering create_app(config_object=%s)", config_object)
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    logger.debug("create_app(config_object=%s): app → %s", config_object, app)
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    logger.debug("<<< Exiting create_app(config_object=%s)", config_object)
    return app


def register_extensions(app):
    logger.debug(">>> Entering register_extensions(app=%s)", app)
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    logger.debug("<<< Exiting register_extensions(app=%s)", app)


def register_blueprints(app):
    logger.debug(">>> Entering register_blueprints(app=%s)", app)
    logger.debug("register_blueprints(app=%s): origins → %s", app, origins)
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(profile.views.blueprint, origins=origins)
    cors.init_app(articles.views.blueprint, origins=origins)
    cors.init_app(reports.views.blueprint, origins=origins)

    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(articles.views.blueprint)
    app.register_blueprint(reports.views.blueprint)
    logger.debug("<<< Exiting register_blueprints(app=%s)", app)


def register_errorhandlers(app):
    logger.debug(">>> Entering register_errorhandlers(app=%s)", app)

    def errorhandler(error):
        logger.debug(">>> Entering errorhandler(error=%s)", error)
        logger.debug("errorhandler(error=%s): response.status_code → %s", error, response.status_code)
        response = error.to_json()
        logger.debug("errorhandler(error=%s): response → %s", error, response)
        response.status_code = error.status_code
        logger.debug("<<< Exiting errorhandler(error=%s)", error)
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


def register_shellcontext(app):
    logger.debug(">>> Entering register_shellcontext(app=%s)", app)
    """Register shell context objects."""
    def shell_context():
        logger.debug(">>> Entering shell_context()")
        """Shell context objects."""
        logger.debug("<<< Exiting shell_context()")
        return {
            'db': db,
            'User': user.models.User,
            'UserProfile': profile.models.UserProfile,
            'Article': articles.models.Article,
            'Tag': articles.models.Tags,
            'Comment': articles.models.Comment,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    logger.debug(">>> Entering register_commands(app=%s)", app)
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    logger.debug("<<< Exiting register_commands(app=%s)", app)
