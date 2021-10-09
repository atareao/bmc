#!/usr/bin/env python3

import sqlite3
import sys
import time

DATABASE = '/app/database/bmc.db'
TABLE_USERS = """
CREATE TABLE IF NOT EXISTS USERS(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
NAME STRING,
EMAIL STRING,
IS_MEMBER INTEGER,
IS_ACTIVE INTEGER,
WAS_WELCOMED INTEGER,
IS_MEMBER_START_TS INTEGER,
IS_ACTIVE_START_TS INTEGER,
WAS_WELCOMED_START_TS INTEGER,
IS_MEMBER_END_TS INTEGER,
IS_ACTIVE_END_TS INTEGER,
WAS_WELCOMED_END_TS INTEGER
)
"""


def logger(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))


def init():
    logger('Create tables in database')
    execute(TABLE_USERS)


def execute(sqlquery, data=None):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        logger(sqlquery)
        if data:
            cursor.execute(sqlquery, data)
        else:
            cursor.execute(sqlquery)
        conn.commit()
    except Exception as e:
        logger(e)
    finally:
        if conn:
            conn.close()


def select(sqlquery, one=False):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(sqlquery)
        if one:
            return cursor.fetchone()
        return cursor.fetchall()
    except Exception as e:
        logger(e)
    finally:
        if conn:
            conn.close()


def check(sqlquery):
    conn = None
