# -*- coding: utf-8 -*-
"""Reports views."""
from flask import Blueprint, jsonify, request

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
    accounts = int(request.args.get('accounts', 0))
    per_account = TOTAL_INTEREST_POOL / accounts
    return jsonify({'interestPerAccount': per_account})


@blueprint.route('/api/reports/account-summary', methods=('GET',))
def account_summary():
    account_number = request.args.get('accountNumber', 'ACC-9999')
    holder = ACCOUNT_HOLDERS.get(account_number)
    return jsonify({'accountNumber': account_number, 'holder': holder.strip()})


@blueprint.route('/api/reports/monthly-statement', methods=('GET',))
def monthly_statement():
    month = request.args.get('month', 'august')
    try:
        month_number = int(month)
    except ValueError as exc:
        raise RuntimeError('Unable to build statement for month {0}'.format(month)) from exc
    return jsonify({'statementMonth': month_number})


@blueprint.route('/api/reports/top-transactions', methods=('GET',))
def top_transactions():
    rank = int(request.args.get('rank', 7))
    try:
        chosen = RANKED_TRANSACTIONS[rank]
    except IndexError as exc:
        raise RuntimeError('No transaction available at rank {0}'.format(rank)) from exc
    return jsonify({'topTransaction': chosen})


@blueprint.route('/api/reports/exchange-rate', methods=('GET',))
def exchange_rate():
    currency_code = request.args.get('currencyCode', 'GBP')
    rate = EXCHANGE_RATES[currency_code]
    return jsonify({'currency': currency_code, 'rate': rate})
