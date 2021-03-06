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
from member import Member
from utils import Log


class BMC:
    def __init__(self, base_uri, token):
        self._base_uri = base_uri
        self._token = token

    def get_active_members(self):
        members = []
        url = f"{self._base_uri}/api/v1/subscriptions?status=active&page=1"
        while url is not None:
            url, new_members = self._get_active_members(url)
            members.extend(new_members)
        return members

    def _get_active_members(self, url):
        members = []
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            Log.info(url)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                Log.info(data)
                url = data['next_page_url']
                for item in data['data']:
                    amember = Member(item['payer_name'], item['payer_email'])
                    members.append(amember)
                return url, members
            else:
                msg = f"Error. HTTP code: {response.status_code}"
                print(response.json())
                raise Exception(msg)
        except Exception as exception:
            Log.error(exception)
        return None, members
