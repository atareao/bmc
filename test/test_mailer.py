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

import unittest
import sys
import os
sys.path.append(os.path.join("../src"))
from mrapi import MailRelay
from utils import Log, load_env


class TestMailer(unittest.TestCase):
    def test_send_mail(self):
        mr = MailRelay(os.environ['BASE_URL'], os.environ['TOKEN'])
        from_name = os.environ['DEFAULT_NAME']
        from_mail = os.environ['DEFAULT_EMAIL']
        to_name = os.environ['TEST_NAME']
        to_mail = os.environ['TEST_EMAIL']
        subject = "Este es de prueba"
        markdown_content = "Hola mundo **cruel** en [aquí](https://atareao.es)"
        mr.send_mail(from_name, from_mail, to_name, to_mail, subject,
                markdown_content)
        self.assertTrue(True)


if __name__ == '__main__':
    load_env("../../bmc_prod.env")
    unittest.main()
