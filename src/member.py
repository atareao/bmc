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

import time
from table import Table
from utils import TRUE, FALSE


class Member(Table):
    TABLE = 'MEMBERS'
    PK = 'ID'
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE}(
        {PK} INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME STRING,
        EMAIL STRING,
        WELCOME INTEGER,
        START INTEGER,
        END INTEGER,
        TIMES
        )
    """
    UNIKEYS = ['EMAIL']

    def __init__(self, name=None, email=None):
        super().__init__()
        if name is not None and email is not None:
            self.NAME = name
            self.EMAIL = email
            self.WELCOME = FALSE
            self.START = 0
            self.END = 0
            self.TIMES = 0

    def start_membership(self):
        self.START = int(time.time())

    def end_membership(self):
        self.END = int(time.time())

    def set_welcomed(self, yes):
        self.WELCOME = TRUE if yes else FALSE

    @classmethod
    def get_by_email(cls, email):
        if email is not None:
            condition = f"EMAIL='{email}'"
            items = cls.select(condition)
            return items[0] if len(items) > 0 else None
        return None

    def exists(self):
        return self.get_by_email(self.EMAIL) is not None
