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


class Supporter(Table):
    TABLE = 'SUPPORTERS'
    PK = 'ID'
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE}(
        {PK} INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME STRING,
        EMAIL STRING,
        THANKS INTEGER,
        LAST_DONATION INTEGER,
        TIMES
        )
    """
    UNIKEYS = ['EMAIL']

    def __init__(self, name=None, email=None):
        super().__init__()
        if name is not None and email is not None:
            self.NAME = name
            self.EMAIL = email
            self.THANKS = FALSE

    def start(self):
        self.LAST_DONATION = int(time.time())
        self.TIMES += 1

    def set_thanks(self, yes):
        self.THANKS = TRUE if yes else FALSE

    @classmethod
    def get_by_email(cls, email):
        if email is not None:
            condition = f"EMAIL='{email}'"
            items = cls.select(condition)
            return items[0] if len(items) > 0 else None
        return None

    def exists(self):
        return self.get_by_email(self.EMAIL) is not None
