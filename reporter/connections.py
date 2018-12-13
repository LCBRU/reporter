#!/usr/bin/env python3

import os
import pymssql
import pymysql.cursors
from contextlib import contextmanager
from enum import Enum

REDCAP_VERSION = '7.2.2'
REDCAP_PATH = 'redcap/redcap_v{}/'.format(REDCAP_VERSION)
REDCAP_UOL_PATH = 'redcap_v{}/'.format(REDCAP_VERSION)
REDCAP_INTERNAL_URL = 'https://briccs.xuhl-tr.nhs.uk/{}'.format(REDCAP_PATH)
REDCAP_EXTERNAL_URL = 'https://uhlbriccsext01.xuhl-tr.nhs.uk/{}'.format(
    REDCAP_PATH)
REDCAP_UOL_CRF_URL = 'https://crf.lcbru.le.ac.uk/{}'.format(
    REDCAP_UOL_PATH)
REDCAP_UOL_SURVEY_URL = 'https://redcap.lcbru.le.ac.uk/{}'.format(
    REDCAP_UOL_PATH)
REDCAP_INTERNAL_DB = 'STG_redcap'
REDCAP_EXTERNAL_DB = 'STG_redcap_briccsext'
REDCAP_UOL_DB = 'redcap'
REDCAP_UOL_SURVEY_DB = 'redcap6170'

OPENSPECIMEN_URL = 'https://catissue-live.lcbru.le.ac.uk/openspecimen/'


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


def get_redcap_uol_crf_link(link_text, project_id, record):
    REDCAP_RECORD_URL = (
        '[{}]({}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_UOL_CRF_URL,
        project_id,
        record))


def get_redcap_uol_survey_link(link_text, project_id, record):
    REDCAP_RECORD_URL = (
        '[{}]({}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_UOL_SURVEY_URL,
        project_id,
        record))


class RedcapInstance(Enum):
    @staticmethod
    def internal():
        return {
            'staging_database': REDCAP_INTERNAL_DB + '.dbo',
            'link_generator': get_redcap_link,
            'base_url': REDCAP_INTERNAL_URL,
            'connection': DatabaseConnection.redcap_internal,
        }

    @staticmethod
    def external():
        return {
            'staging_database': REDCAP_EXTERNAL_DB + '.dbo',
            'link_generator': get_redcap_external_link,
            'base_url': REDCAP_EXTERNAL_URL,
            'connection': DatabaseConnection.redcap_external,
        }

    @staticmethod
    def uol_lamp():
        return {
            'staging_database': 'redcap',
            'link_generator': get_redcap_uol_crf_link,
            'base_url': REDCAP_INTERNAL_URL,
            'connection': DatabaseConnection.uol_lamp,
        }

    @staticmethod
    def uol_survey():
        return {
            'staging_database': 'redcap',
            'link_generator': get_redcap_uol_survey_link,
            'base_url': REDCAP_INTERNAL_URL,
            'connection': DatabaseConnection.uol_survey,
        }


def get_openspecimen_link(
    link_text,
    collection_protocol_id,
    collection_protocol_reg_id,
):

    OS_PARTICIPANT_URL = (
        '[{}]({}#/cp-view/{}/participants/{}/detail/overview)'
    )

    return (OS_PARTICIPANT_URL.format(
        link_text,
        OPENSPECIMEN_URL,
        collection_protocol_id,
        collection_protocol_reg_id))


class OpenSpecimenInstance(Enum):
    @staticmethod
    def live():
        return {
            'link_generator': get_openspecimen_link,
        }


class DatabaseConnection(Enum):

    @staticmethod
    @contextmanager
    def reporting():
        conn = pymssql.connect(
            host=os.environ["SQL_REPORTING_HOST"],
            user=os.environ["SQL_REPORTING_USER"],
            password=os.environ["SQL_REPORTING_PASSWORD"],
            database=os.environ["SQL_REPORTING_DATABASE"],
        )

        try:

            with conn.cursor(as_dict=True) as cursor:
                yield cursor

        finally:
            conn.close()

    @staticmethod
    @contextmanager
    def redcap_internal():
        conn = pymssql.connect(
            host=os.environ["SQL_REPORTING_HOST"],
            user=os.environ["SQL_REPORTING_USER"],
            password=os.environ["SQL_REPORTING_PASSWORD"],
            database=REDCAP_INTERNAL_DB,
        )

        try:

            with conn.cursor(as_dict=True) as cursor:
                yield cursor

        finally:
            conn.close()

    @staticmethod
    @contextmanager
    def redcap_external():
        conn = pymssql.connect(
            host=os.environ["SQL_REPORTING_HOST"],
            user=os.environ["SQL_REPORTING_USER"],
            password=os.environ["SQL_REPORTING_PASSWORD"],
            database=REDCAP_EXTERNAL_DB,
        )

        try:

            with conn.cursor(as_dict=True) as cursor:
                yield cursor

        finally:
            conn.close()

    @staticmethod
    @contextmanager
    def dwbriccs():
        conn = pymssql.connect(
            host=os.environ["SQL_DWBRICCS_HOST"],
            user=os.environ["SQL_DWBRICCS_USER"],
            password=os.environ["SQL_DWBRICCS_PASSWORD"],
            database=os.environ["SQL_DWBRICCS_DATABASE"],
        )

        try:

            with conn.cursor(as_dict=True) as cursor:
                yield cursor

        finally:
            conn.close()

    @staticmethod
    @contextmanager
    def uol_lamp():

        conn = pymysql.connect(
            host=os.environ["SQL_REPORTING_HOST"],
            port=int(os.environ.get("SQL_REPORTING_PORT", '3306')),
            user=os.environ["SQL_REPORTING_USER"],
            database=REDCAP_UOL_DB,
            password=os.environ["SQL_REPORTING_PASSWORD"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:

            with conn.cursor() as cursor:
                yield cursor

        finally:
            conn.close()

    @staticmethod
    @contextmanager
    def uol_survey():

        conn = pymysql.connect(
            host=os.environ["SQL_REPORTING_HOST"],
            port=int(os.environ.get("SQL_REPORTING_PORT", '3306')),
            user=os.environ["SQL_REPORTING_USER"],
            database=REDCAP_UOL_SURVEY_DB,
            password=os.environ["SQL_REPORTING_PASSWORD"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:

            with conn.cursor() as cursor:
                yield cursor

        finally:
            conn.close()
