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

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from markdown import Markdown
from io import StringIO


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


class Mailer:
    def __init__(self, server, port, mail, password):
        self._server = server
        self._port = port
        self._mail = mail
        self._password = password

    @classmethod
    def to_plain(cls, text_in_markdown):
        Markdown.output_formats["plain"] = unmark_element
        md = Markdown(output_format="plain")
        md.stripTopLevelTags = False
        return md.convert(text_in_markdown)

    @classmethod
    def to_html(cls, text_in_markdown):
        md = Markdown()
        return md.convert(text_in_markdown)

    def send(self, to, subject, text_in_markdown):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self._mail
        message["To"] = to

        text = Mailer.to_plain(text_in_markdown)
        html = Mailer.to_html(text_in_markdown)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        print(self._server, self._port)
        with smtplib.SMTP_SSL(self._server,
                              self._port,
                              context=context) as server:
            server.login(self._mail, self._password)
            server.sendmail(self._mail, to, message.as_string())
