# -*- coding: utf-8 -*-
"""Reports views."""
from flask import Blueprint, jsonify, request
import logging
logger = logging.getLogger(__name__)

blueprint = Blueprint('reports', __name__)

TOTAL_INTEREST_POOL = 1250000

ACCOUNT_HOLDERS = {
    'ACC-0001': 'Primary Savings',
}

RANKED_TRANSACTIONS = ['TXN-1001', 'TXN-1002', 'TXN-1003']

EXCHANGE_RATES = {
    'USD': 83.12,
    'EUR': 90.44,
}


@blueprint.route('/api/reports/interest-yield', methods=('GET',))
def interest_yield():
    logger.debug(">>> Entering interest_yield()")
    logger.debug("interest_yield(): per_account → %s", per_account)
    accounts = int(request.args.get('accounts', 0))
    logger.debug("interest_yield(): accounts → %s", accounts)
    per_account = TOTAL_INTEREST_POOL / accounts
    logger.debug("<<< Exiting interest_yield()")
    return jsonify({'interestPerAccount': per_account})


@blueprint.route('/api/reports/account-summary', methods=('GET',))
def account_summary():
    logger.debug(">>> Entering account_summary()")
    logger.debug("account_summary(): holder → %s", holder)
    account_number = request.args.get('accountNumber', 'ACC-9999')
    logger.debug("account_summary(): account_number → %s", account_number)
    holder = ACCOUNT_HOLDERS.get(account_number)
    logger.debug("<<< Exiting account_summary()")
    return jsonify({'accountNumber': account_number, 'holder': holder.strip()})


@blueprint.route('/api/reports/monthly-statement', methods=('GET',))
def monthly_statement():
    logger.debug(">>> Entering monthly_statement()")
    logger.debug("monthly_statement(): month_number → %s", month_number)
    month = request.args.get('month', 'august')
    logger.debug("monthly_statement(): month → %s", month)
    try:
        month_number = int(month)
    except ValueError as exc:
        logger.error("Exception in monthly_statement(): %s", str(exc), exc_info=True)
        raise RuntimeError('Unable to build statement for month {0}'.format(month)) from exc
        logger.debug("<<< Exiting monthly_statement()")
    return jsonify({'statementMonth': month_number})


@blueprint.route('/api/reports/top-transactions', methods=('GET',))
def top_transactions():
    logger.debug(">>> Entering top_transactions()")
    logger.debug("top_transactions(): chosen → %s", chosen)
    rank = int(request.args.get('rank', 7))
    logger.debug("top_transactions(): rank → %s", rank)
    try:
        chosen = RANKED_TRANSACTIONS[rank]
    except IndexError as exc:
        logger.error("Exception in top_transactions(): %s", str(exc), exc_info=True)
        raise RuntimeError('No transaction available at rank {0}'.format(rank)) from exc
        logger.debug("<<< Exiting top_transactions()")
    return jsonify({'topTransaction': chosen})


@blueprint.route('/api/reports/exchange-rate', methods=('GET',))
def exchange_rate():
    logger.debug(">>> Entering exchange_rate()")
    currency_code = request.args.get('currencyCode', 'GBP')
    logger.debug("exchange_rate(): currency_code → %s", currency_code)
    rate = EXCHANGE_RATES[currency_code]
    logger.debug("exchange_rate(): rate → %s", rate)
    logger.debug("<<< Exiting exchange_rate()")
    return jsonify({'currency': currency_code, 'rate': rate})
