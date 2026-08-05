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

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    logger.debug(">>> Entering test()")
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)

    logger.debug("<<< Exiting test()")

@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint(fix_imports):
    logger.debug(">>> Entering lint(fix_imports=%s)", fix_imports)
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    logger.debug("lint(fix_imports=%s): skip → %s", fix_imports, skip)
    logger.debug("lint(fix_imports=%s): root_files → %s", fix_imports, root_files)
    logger.debug("lint(fix_imports=%s): root_directories → %s", fix_imports, root_directories)
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        logger.debug(">>> Entering execute_tool(description=%s)", description)
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        logger.debug("execute_tool(description=%s): command_line → %s", description, command_line)
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

            logger.debug("<<< Exiting execute_tool(description=%s)", description)
    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
def clean():
    logger.debug(">>> Entering clean()")
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, _, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)

                logger.debug("clean(): full_pathname → %s", full_pathname)

@click.command()
@click.option('--url', default=None,
              help='Url to test (ex. /static/image.png)')
@click.option('--order', default='rule',
              help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):
    logger.debug(">>> Entering urls(url=%s,order=%s)", url, order)
    """Display all of the url matching routes for the project.

    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    logger.debug("urls(url=%s,order=%s): rows → %s", url, order, rows)
    logger.debug("urls(url=%s,order=%s): column_headers → %s", url, order, column_headers)
    column_headers = ('Rule', 'Endpoint', 'Arguments')

    if url:
        try:
            rule, arguments = (
                current_app.url_map.bind('localhost')
                .match(url, return_rule=True))
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
            logger.debug("urls(url=%s,order=%s): column_length → %s", url, order, column_length)
        except (NotFound, MethodNotAllowed) as e:
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1
            logger.error("Exception in urls(url=%s,order=%s): %s", url, order, str(e), exc_info=True)
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        for rule in rules:
            logger.debug("urls(url=%s,order=%s): rules → %s", url, order, rules)
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ''
    logger.debug("urls(url=%s,order=%s): str_template → %s", url, order, str_template)
    logger.debug("urls(url=%s,order=%s): table_width → %s", url, order, table_width)
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        logger.debug("urls(url=%s,order=%s): max_rule_length → %s", url, order, max_rule_length)
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        logger.debug("urls(url=%s,order=%s): max_endpoint_length → %s", url, order, max_endpoint_length)
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        logger.debug("urls(url=%s,order=%s): max_arguments_length → %s", url, order, max_arguments_length)
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo('-' * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))
