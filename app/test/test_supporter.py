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
from supporter import Supporter
from utils import Log, TRUE, FALSE

Supporter.DATABASE = 'test.db'


class TestSupporter(unittest.TestCase):
    def setUp(self):
        if os.path.exists(Supporter.DATABASE):
            os.remove(Supporter.DATABASE)
        Supporter.inicializate()

    def tearDown(self):
        if os.path.exists(Supporter.DATABASE):
            os.remove(Supporter.DATABASE)

    def test_create(self):
        Log.info("=== test_create ===")
        asupporter = Supporter("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        asupporter.save()
        nsupporter = Supporter.get_by_id(asupporter.ID)
        nsupporter.save()
        self.assertEqual(asupporter, nsupporter)

    def test_compare(self):
        Log.info("=== test_create ===")
        asupporter = Supporter("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        asupporter.save()
        bsupporter = Supporter("Lorenzo", "atareao@atareao.es")
        bsupporter.save()
        self.assertNotEqual(asupporter, bsupporter)

    def test_donation(self):
        Log.info("=== donation ===")
        asupporter = Supporter("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        asupporter.save()
        asupporter.start()
        asupporter.start()
        asupporter.start()
        asupporter.save()
        rsupporter = Supporter.get_by_id(asupporter.ID)
        self.assertEqual(rsupporter.TIMES, 3)

    def test_welcome(self):
        Log.info("=== test_create ===")
        asupporter = Supporter("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        asupporter.save()
        self.assertEqual(asupporter.THANKS, FALSE)
        asupporter.set_thanks(True)
        asupporter.save()
        nsupporter = Supporter.get_by_id(asupporter.ID)
        self.assertEqual(nsupporter.THANKS, TRUE)



if __name__ == '__main__':
    unittest.main()
