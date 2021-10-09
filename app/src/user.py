#!/usr/bin/env python3

from time import time
from apidb import execute, select, logger

TRUE = 0
FALSE = 1

class User:
    def __init__(self, name, email):
        self.id = -1
        self.name = name
        self.email = email
        self.is_member = False
        self.is_active = False
        self.was_welcomed = False
        self._is_member_start_ts = 0
        self._is_active_start_ts = 0
        self._was_welcomed_start_ts = 0
        self._is_member_end_ts = 0
        self._is_active_end_ts = 0
        self._was_welcomed_end_ts = 0

    @classmethod
    def from_json(cls, item):
        return User(item['payer_name'], item['payer_email'])

    @classmethod
    def from_db(cls, item):
        an_user = User(None, None)
        an_user.id = item[0]
        an_user.name = item[1]
        an_user.email = item[2]
        an_user._is_member = item[3]
        an_user._is_active = item[4]
        an_user._was_welcomed = item[5]
        an_user._is_member_start_ts = item[6]
        an_user._is_active_start_ts = item[7]
        an_user._was_welcomed_start_ts = item[8]
        an_user._is_member_end_ts = item[9]
        an_user._is_active_end_ts = item[10]
        an_user._was_welcomed_end_ts = item[11]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def is_member(self):
        return self._is_member == TRUE

    @is_member.setter
    def is_member(self, value):
        if value is True:
            self._is_member = TRUE
            self.is_member_start_ts = int(time())
        else:
            self._is_member = FALSE
            self.is_member_end_ts = int(time())

    @property
    def is_active(self):
        return self._is_active == TRUE

    @is_active.setter
    def is_active(self, value):
        if value is True:
            self._is_active = TRUE
            self.is_active_start_ts = int(time())
        else:
            self._is_active = FALSE
            self.is_active_end_ts = int(time())

    @property
    def was_welcomed(self):
        return self._was_welcomed == TRUE

    @was_welcomed.setter
    def was_welcomed(self, value):
        if value is True:
            self._was_welcomed = TRUE
            self.was_welcomed_start_ts = int(time())
        else:
            self._was_welcomed = FALSE
            self.was_welcomed_end_ts = int(time())

    @property
    def is_member_start_ts(self):
        return self._is_member_start_ts

    @is_member_start_ts.setter
    def is_member_start_ts(self, value):
        self._is_member_start_ts = value

    @property
    def is_active_start_ts(self):
        return self._is_active_start_ts

    @is_active_start_ts.setter
    def is_active_start_ts(self, value):
        self._is_active_start_ts = value

    @property
    def was_welcomed_start_ts(self):
        return self._was_welcomed_start_ts

    @was_welcomed_start_ts.setter
    def was_welcomed_start_ts(self, value):
        self._was_welcomed_start_ts = value

    @property
    def is_member_end_ts(self):
        return self._is_member_end_ts

    @is_member_end_ts.setter
    def is_member_end_ts(self, value):
        self._is_member_end_ts = value

    @property
    def is_active_end_ts(self):
        return self._is_active_end_ts

    @is_active_end_ts.setter
    def is_active_end_ts(self, value):
        self._is_active_end_ts = value

    @property
    def was_welcomed_end_ts(self):
        return self._was_welcomed_end_ts

    @was_welcomed_end_ts.setter
    def was_welcomed_end_ts(self, value):
        self._was_welcomed_end_ts = value

    def save(self):
        if self.id != -1:
            sqlquery = """
UPDATE USERS SET NAME=?, EMAIL=?, IS_MEMBER=?, IS_ACTIVE=?, WAS_WELCOMED=?,
IS_MEMBER_START_TS=?, IS_ACTIVE_START_TS=?, WAS_WELCOMED_START_TS=?,
IS_MEMBER_END_TS=?, IS_ACTIVE_END_TS=?, WAS_WELCOMED_END_TS=? WHERE ID=?
"""
            logger(sqlquery)
            data = (self.name, self.email, self.is_member, self.is_active,
                    self.was_welcomed, self.is_member_start_ts,
                    self.is_active_start_ts, self.was_welcomed_start_ts,
                    self.is_member_end_ts, self.is_active_end_ts,
                    self.was_welcomed_end_ts, self.id)
        else:
            sqlquery = """
INSERT INTO USERS (NAME, EMAIL, IS_MEMBER, IS_ACTIVE, WAS_WELCOMED,
IS_MEMBER_START_TS, IS_ACTIVE_START_TS, WAS_WELCOMED_START_TS,
IS_ACTIVE_END_TS, IS_ACTIVE_END_TS, WAS_WELCOMED_END_TS) VALUES (
?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
            logger(sqlquery)
            data = (self.name, self.email, self.is_member, self.is_active,
                    self.was_welcomed, self.is_member_start_ts,
                    self.is_active_start_ts, self.was_welcomed_start_ts,
                    self.is_member_end_ts, self.is_active_end_ts,
                    self.was_welcomed_end_ts)
        execute(sqlquery, data)

    @classmethod
    def get_user_by_id(cls, id):
        sqlquery = f"SELECT * FROM USERS WHERE ID='{id}'"
        logger(sqlquery)
        result = select(sqlquery, True)
        if result:
            return cls.from_db(result)
        return None

    @classmethod
    def get_user_by_email(cls, email):
        if email is not None:
            sqlquery = f"SELECT * FROM USERS WHERE EMAIL='{email}'"
            logger(sqlquery)
            result = select(sqlquery, True)
            if result:
                return cls.from_db(result)
        return None

    @classmethod
    def exists(cls, email):
        return cls.get_user_by_email(email) is not None

    @classmethod
    def get_users(cls):
        users = []
        sqlquery = 'SELECT * FROM USERS'
        logger(sqlquery)
        result =select(sqlquery)
        if result:
            for item in result:
                users.append(cls.from_db(item))
        return users

    @classmethod
    def insert_user(cls, ):
        users = []
        sqlquery = 'SELECT * FROM USERS'
        logger(sqlquery)
        result =select(sqlquery)
        if result:
            for item in result:
                users.append(cls.from_db(item))
        return users

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Email: {self.email}\n" \
               f"Is member: {self.is_member}\n" \
               f"Is active: {self.is_active}\n" \
               f"Was welcomed: {self.was_welcomed}\n" \
               f"Is member from: {self.is_member_start_ts}"

    def __eq__(self, other):
        return self.email == other.email
