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

import requests
import json
from utils import Log

class Telegram:
    URL = 'https://api.telegram.org/bot{}'

    def __init__(self, token):
        self._token = token

    def send_poll(self, chat_id, aquestion):
        url = self.URL.format(self._token) + '/sendPoll'
        data = {'chat_id': chat_id, 
                'question': aquestion.question,
                'options': json.dumps(aquestion.options.split('|')),
                'type': 'quiz',
                'correct_option_id': aquestion.correct_option}
        response = requests.post(url, data=data)
        Log.info(f"Código de respuesta: {response.status_code}")
        Log.info(f"Content: {response.text}")
