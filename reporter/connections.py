#!/usr/bin/env python3

import os
import pymssql
import pymysql.cursors
from contextlib import contextmanager
from enum import Enum

REDCAP_VERSION = '7.2.2'
REDCAP_PATH = 'redcap/redcap_v{}/'.format(REDCAP_VERSION)
REDCAP_INTERNAL_URL = 'https://briccs.xuhl-tr.nhs.uk/{}'.format(REDCAP_PATH)
REDCAP_EXTERNAL_URL = 'https://uhlbriccsext01.xuhl-tr.nhs.uk/{}'.format(
    REDCAP_PATH)

SQL_REPORTING_HOST = os.environ.get("SQL_REPORTING_HOST", '')
SQL_REPORTING_USER = os.environ.get("SQL_REPORTING_USER", '')
SQL_REPORTING_PASSWORD = os.environ.get("SQL_REPORTING_PASSWORD", '')
SQL_REPORTING_DATABASE = os.environ.get("SQL_REPORTING_DATABASE", '')

SQL_DWBRICCS_HOST = os.environ.get("SQL_DWBRICCS_HOST", '')
SQL_DWBRICCS_USER = os.environ.get("SQL_DWBRICCS_USER", '')
SQL_DWBRICCS_PASSWORD = os.environ.get("SQL_DWBRICCS_PASSWORD", '')
SQL_DWBRICCS_DATABASE = os.environ.get("SQL_DWBRICCS_DATABASE", '')


def get_redcap_link(link_text, project_id, record):
    REDCAP_RECORD_URL = (
        '[{}]({}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_INTERNAL_URL,
        project_id,
        record))


def get_redcap_external_link(link_text, project_id, record):
    REDCAP_RECORD_URL = (
        '[{}]({}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_EXTERNAL_URL,
        project_id,
        record))


class RedcapInstance(Enum):
    def internal():
        return {
            'staging_database': 'STG_redcap',
            'link_generator': get_redcap_link,
            'base_url': REDCAP_INTERNAL_URL,
        }

    def external():
        return {
            'staging_database': 'STG_redcap_briccsext',
            'link_generator': get_redcap_external_link,
            'base_url': REDCAP_EXTERNAL_URL,
        }

    def uol_lamp():
        return {
            'staging_database': 'redcap',
            'link_generator': get_redcap_link,
            'base_url': REDCAP_INTERNAL_URL,
        }


class DatabaseConnection(Enum):

    @contextmanager
    def reporting():
        conn = pymssql.connect(
            SQL_REPORTING_HOST,
            SQL_REPORTING_USER,
            SQL_REPORTING_PASSWORD,
            SQL_REPORTING_DATABASE,
        )

        try:

            with conn.cursor(as_dict=True) as cursor:
                yield cursor

        finally:
            conn.close()

    @contextmanager
    def dwbriccs():
        conn = pymssql.connect(
            SQL_DWBRICCS_HOST,
            SQL_DWBRICCS_USER,
            SQL_DWBRICCS_PASSWORD,
            SQL_DWBRICCS_DATABASE
        )

        try:

            with conn.cursor(as_dict=True) as cursor:
                yield cursor

        finally:
            conn.close()

    @contextmanager
    def uol_lamp():

        conn = pymysql.connect(
            host=SQL_REPORTING_HOST,
            user=SQL_REPORTING_USER,
            password=SQL_REPORTING_PASSWORD,
            db=SQL_REPORTING_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:

            with conn.cursor() as cursor:
                yield cursor

        finally:
            conn.close()
