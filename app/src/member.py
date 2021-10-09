#!/usr/bin/env python3

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
