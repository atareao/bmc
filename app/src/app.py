#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
import hmac
import hashlib
from flask import Flask, jsonify, make_response, request
from table import Table
from member import Member
from supporter import Supporter
from utils import Log, TRUE, FALSE
from bmc import BMC
from mrapi import MailRelay
from letterwriter import LetterWriter


app = Flask(__name__)

if os.environ['ENVIRONMENT'] == 'TEST':
    Table.DATABASE = '/app/database/test.db'
else:
    Table.DATABASE = '/app/database/bmc.db'
Log.set(os.environ['DEBUG'])


@app.route('/status', methods=['GET'])
def get_status():
    return make_response(jsonify({'status': 'Up and running'}), 200)


@app.route('/bmc/webhook/<webhook>', methods=['POST'])
def bmc_webhook(webhook):
    if os.environ['WEBHOOK'] == webhook:
        headers = request.headers
        if 'User-Agent' in headers and \
                'X-Bmc-Event' in headers and \
                'X-Bmc-Signature' in headers and \
                headers['User-Agent'] == 'BMC-HTTPS-ROBOT':
            secret = os.environ['BMC_SECRET']
            signature = hmac.new(bytes(secret, 'latin-1'),
                                 msg=request.data,
                                 digestmod=hashlib.sha256).hexdigest()
            if headers['X-Bmc-Signature'] == signature:
                payload = request.json
                if 'response' in payload:
                    supporter_email = payload['response']['supporter_email']
                    supporter_name = payload['response']['supporter_name']
                    template = '/app/templates/donacion.md'
                    tokens = {"name": supporter_name,
                              "email": supporter_email}
                    awriter = LetterWriter(template, tokens)
                    content = awriter.format()
                    subject = os.environ['DEFAULT_SUBJECT']
                    asupporter = Supporter.get_by_email(supporter_email)
                    if asupporter is None:
                        asupporter = Supporter(supporter_name, supporter_email)
                    asupporter.start()
                    try:
                        if os.environ['ENVIRONMENT'] == 'TEST':
                            to_email = os.environ['TEST_EMAIL']
                        else:
                            to_email = asupporter.EMAIL
                        amailer = MailRelay(os.environ['BASE_URL'],
                                            os.environ['TOKEN'])
                        amailer.send_mail(os.environ['DEFAULT_NAME'],
                                          os.environ['DEFAULT_EMAIL'],
                                          asupporter.NAME,
                                          to_email,
                                          subject,
                                          content)
                        asupporter.set_thanks(True)
                    except Exception as exception:
                        Log.error(exception)
                        asupporter.set_thanks(False)
                    Log.info("New donation {}".format(user.name))
                    asupporter.save()
                return make_response(jsonify({'status': 'Updated'}), 200)
    return make_response(jsonify({'status': 'error', 'msg': 'Not found'}), 404)


@app.route('/discord/<webhook>', methods=['POST'])
def discord_webhook(webhook):
    if os.environ['WEBHOOK'] != webhook:
        return make_response(jsonify({'status': 'error',
                             'msg': 'Not found'}), 404)
    else:
        Log.info(request.headers)
        Log.info(request.data)
    return make_response(jsonify({'status': 'OK',
                                  'msg': 'Up and running'}), 200)


@app.route('/bmc/update/<webhook>', methods=['GET'])
def bmc_update(webhook):
    if os.environ['WEBHOOK'] != webhook:
        return make_response(jsonify({'status': 'error',
                             'msg': 'Not found'}), 404)
    else:
        bmc = BMC(os.environ["BMC_BASE_URI"],
                  os.environ["BMC_ACCESS_TOKEN"])
        bmc_members = bmc.get_active_members()
        for bmc_member in bmc_members:
            amember = Member.get_by_email(bmc_member.EMAIL)
            if amember and amember.WELCOME == TRUE:
                continue
            if amember is None:
                amember = Member(bmc_member.NAME, bmc_member.EMAIL)
                amember.start_membership()
            template = '/app/templates/suscripcion.md'
            tokens = {"name": amember.NAME,
                      "email": amember.EMAIL}
            awriter = LetterWriter(template, tokens)
            content = awriter.format()
            amailer = MailRelay(os.environ['BASE_URL'],
                                os.environ['TOKEN'])
            subject = "Infinitas gracias por tu apoyo a atareao.es"
            try:
                if os.environ['ENVIRONMENT'] == 'TEST':
                    to_email = os.environ['TEST_EMAIL']
                else:
                    to_email = amember.EMAIL
                amailer.send_mail(os.environ['DEFAULT_NAME'],
                                  os.environ['DEFAULT_EMAIL'],
                                  amember.NAME,
                                  to_email,
                                  subject,
                                  content)
                amember.set_welcomed(True)
            except Exception as exception:
                amember.set_welcomed(False)
                Log.error(exception)
            Log.info("New member {}".format(amember.NAME))
            amember.save()
        return make_response(jsonify({'status': 'OK', 'msg': 'Updated'}), 200)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status': 'error', 'msg': 'Not found'}), 404)


def init():
    Member.inicializate()
    Supporter.inicializate()

if __name__ == '__main__':
    init()
    app.run(debug=True, host='0.0.0.0')
