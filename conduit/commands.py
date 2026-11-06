# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound
import logging
logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    logger.debug("test(): rv → %s", rv, extra={"event.action": "test"})
    exit(rv)
    logger.debug("<<< Exiting test()", extra={"event.action": "test"})


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    logger.debug("lint(fix_imports=%s): skip → %s", fix_imports, skip, extra={"event.action": "lint", "logrite.fix_imports": fix_imports})
    root_files = glob('*.py')
    logger.debug("lint(fix_imports=%s): root_files → %s", fix_imports, root_files, extra={"event.action": "lint", "logrite.fix_imports": fix_imports})
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    logger.debug("lint(fix_imports=%s): root_directories → %s", fix_imports, root_directories, extra={"event.action": "lint", "logrite.fix_imports": fix_imports})
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]
    logger.debug("lint(fix_imports=%s): files_and_directories → %s", fix_imports, files_and_directories, extra={"event.action": "lint", "logrite.fix_imports": fix_imports})

    logger.debug("<<< Exiting lint(fix_imports=%s)", fix_imports, extra={"event.action": "lint", "logrite.fix_imports": fix_imports})
    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        logger.debug("execute_tool(description=%s): command_line → %s", description, command_line, extra={"event.action": "execute_tool", "logrite.description": description})
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        logger.debug("execute_tool(description=%s): rv → %s", description, rv, extra={"event.action": "execute_tool", "logrite.description": description})
        if rv != 0:
            exit(rv)
            logger.debug("<<< Exiting execute_tool(description=%s)", description, extra={"event.action": "execute_tool", "logrite.description": description})

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                logger.debug("clean(): full_pathname → %s", full_pathname, extra={"event.action": "clean"})
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)
                logger.debug("<<< Exiting clean()", extra={"event.action": "clean"})


@click.command()
@click.option('--url', default=None,
              help='Url to test (ex. /static/image.png)')
@click.option('--order', default='rule',
              help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.

    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    logger.debug("urls(url=%s,order=%s): rows → %s", url, order, rows, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})
    column_headers = ('Rule', 'Endpoint', 'Arguments')
    logger.debug("urls(url=%s,order=%s): column_headers → %s", url, order, column_headers, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})

    if url:
        try:
            rule, arguments = (
                current_app.url_map.bind('localhost')
                .match(url, return_rule=True))
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            logger.warning("Exception in urls(url=%s,order=%s): %s", url, order, str(e), exc_info=True, extra={"event.action": "urls", "event.category": "process", "logrite.url": url, "logrite.order": order})
            logger.debug("urls(url=%s,order=%s): column_length → %s", url, order, column_length, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        logger.warning("urls(url=%s,order=%s): key → %s", url, order, key, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ''
    logger.debug("urls(url=%s,order=%s): str_template → %s", url, order, str_template, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})
    table_width = 0
    logger.debug("urls(url=%s,order=%s): table_width → %s", url, order, table_width, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        logger.debug("urls(url=%s,order=%s): max_rule_length → %s", url, order, max_rule_length, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo('-' * table_width)

    for row in rows:
        logger.debug("<<< Exiting urls(url=%s,order=%s)", url, order, extra={"event.action": "urls", "logrite.url": url, "logrite.order": order})
        click.echo(str_template.format(*row[:column_length]))
