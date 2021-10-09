#!/usr/bin/env python3
import os
from flask import Flask, jsonify, make_response
from apidb import init, check, logger
from user import User
from bmc import BMC

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def get_status():
    return 'Up and running', 201


@app.route('/<webhook>/bmc_webhook', methods=['POST'])
def bmc_webhook(webhook):
    if os.environ['WEBHOOK'] != webhook:
        return 'KO', 404
    else:
        logger(request.json)


@app.route('/<webhook>/bmc_update', methods=['GET'])
def bmc_update(webhook):
    if os.environ['WEBHOOK'] != webhook:
        return 'KO', 404
    else:
        bmc = BMC(os.environ["BMC_ACCESS_TOKEN"])
        users = bmc.get_active_members()
        for user in users:
            if User.exists(user.email) is False:
                user.save()
        return 'Updated', 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    if not check('SELECT * FROM USERS'):
        init()
    app.run(debug=True, host='0.0.0.0')
