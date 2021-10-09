#!/usr/bin/env python3

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
