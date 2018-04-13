#!/usr/bin/env python3

import os
import pymssql
from enum import Enum

REDCAP_VERSION = '7.2.2'
REDCAP_PATH = 'redcap/redcap_v{}/'.format(REDCAP_VERSION)
REDCAP_INTERNAL_URL = 'https://briccs.xuhl-tr.nhs.uk/{}'.format(REDCAP_PATH)
REDCAP_EXTERNAL_URL = 'https://uhlbriccsext01.xuhl-tr.nhs.uk/{}'.format(
    REDCAP_PATH)

SQL_REPORTING_HOST = os.environ["SQL_REPORTING_HOST"]
SQL_REPORTING_USER = os.environ["SQL_REPORTING_USER"]
SQL_REPORTING_PASSWORD = os.environ["SQL_REPORTING_PASSWORD"]
SQL_REPORTING_DATABASE = os.environ["SQL_REPORTING_DATABASE"]

SQL_DWBRICCS_HOST = os.environ["SQL_DWBRICCS_HOST"]
SQL_DWBRICCS_USER = os.environ["SQL_DWBRICCS_USER"]
SQL_DWBRICCS_PASSWORD = os.environ["SQL_DWBRICCS_PASSWORD"]
SQL_DWBRICCS_DATABASE = os.environ["SQL_DWBRICCS_DATABASE"]


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


class DatabaseConnection(Enum):
    def reporting():
        return pymssql.connect(
            SQL_REPORTING_HOST,
            SQL_REPORTING_USER,
            SQL_REPORTING_PASSWORD,
            SQL_REPORTING_DATABASE
        )

    def dwbriccs():
        return pymssql.connect(
            SQL_DWBRICCS_HOST,
            SQL_DWBRICCS_USER,
            SQL_DWBRICCS_PASSWORD,
            SQL_DWBRICCS_DATABASE
        )
