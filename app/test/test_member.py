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
from member import Member
from utils import Log, TRUE, FALSE

Member.DATABASE = 'test.db'


class TestMember(unittest.TestCase):
    def setUp(self):
        if os.path.exists(Member.DATABASE):
            os.remove(Member.DATABASE)
        Member.inicializate()

    def tearDown(self):
        if os.path.exists(Member.DATABASE):
            os.remove(Member.DATABASE)

    def test_create(self):
        Log.info("=== test_create ===")
        amember = Member("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        amember.save()
        nmember = Member.get_by_id(amember.ID)
        nmember.save()
        self.assertEqual(amember, nmember)

    def test_compare(self):
        Log.info("=== test_create ===")
        amember = Member("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        amember.save()
        bmember = Member("Lorenzo", "atareao@atareao.es")
        bmember.save()
        self.assertNotEqual(amember, bmember)

    def test_welcome(self):
        Log.info("=== test_create ===")
        amember = Member("Lorenzo", "lorenzo.carbonell.cerezo@gmail.com")
        amember.save()
        self.assertEqual(amember.WELCOME, FALSE)
        amember.set_welcomed(True)
        amember.save()
        nmember = Member.get_by_id(amember.ID)
        self.assertEqual(nmember.WELCOME, TRUE)



if __name__ == '__main__':
    unittest.main()
