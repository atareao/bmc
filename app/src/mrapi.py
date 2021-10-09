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
from markdown import Markdown
from io import StringIO


class MailRelay:
    def __init__(self, base_url, token):
        self._base_url = base_url
        self._token = token

    @staticmethod
    def unmark_element(element, stream=None):
        if stream is None:
            stream = StringIO()
        if element.text:
            stream.write(element.text)
        for sub in element:
            MailRelay.unmark_element(sub, stream)
        if element.tail:
            stream.write(element.tail)
        return stream.getvalue()

    @staticmethod
    def to_plain(markdown_content):
        Markdown.output_formats["plain"] = MailRelay.unmark_element
        md = Markdown(output_format="plain")
        md.stripTopLevelTags = False
        return md.convert(markdown_content)

    @staticmethod
    def to_html(markdown_content):
        md = Markdown()
        return md.convert(markdown_content)

    def send_mail(self, from_name, from_mail, to_name, to_mail, subject,
            markdown_content):
        payload = {
                "from": {"email": from_mail, "name": from_name},
                "to": [{"email": to_mail, "name": to_name}],
                "subject": subject,
                "html_part": MailRelay.to_html(markdown_content),
                "text_part": MailRelay.to_plain(markdown_content)
                }
        headers = {
                'content-type': 'application/json',
                'x-auth-token': self._token
                }
        url = f"{self._base_url}/send_emails"
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print(response.raw)
                return True
        except Exception as exception:
            print(exception)
        return False

if __name__ == '__main__':
    base_url = 'https://atareao.ipzmarketing.com/api/v1'
    token = 'A8Z7eCl5iC7YTgBKPJyujKvkCncyklzlkOjERKA0'
    from_name = "lorenzo"
    from_mail = "atareao@atareao.es"
    to_name = "carbonelo"
    to_mail = "lorenzo.carbonell.cerezo@gmail.com"
    subject = "Correo de test with API"
    markdown_content = "Este es un *correo* de prueba, mister **Carbonelo**"
    mailrelay = MailRelay(base_url, token)
    mailrelay.send_mail(from_name, from_mail, to_name, to_mail, subject,
            markdown_content)

