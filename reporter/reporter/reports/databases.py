#!/usr/bin/env python3

import os
import pymssql
from enum import Enum
from reporter.reports.redcap import (
    get_redcap_link,
    get_redcap_external_link,
    BASE_URL_INTERNAL,
    BASE_URL_EXTERNAL,
)


SQL_REPORTING_HOST = os.environ["SQL_REPORTING_HOST"]
SQL_REPORTING_USER = os.environ["SQL_REPORTING_USER"]
SQL_REPORTING_PASSWORD = os.environ["SQL_REPORTING_PASSWORD"]
SQL_REPORTING_DATABASE = os.environ["SQL_REPORTING_DATABASE"]

SQL_DWBRICCS_HOST = os.environ["SQL_DWBRICCS_HOST"]
SQL_DWBRICCS_USER = os.environ["SQL_DWBRICCS_USER"]
SQL_DWBRICCS_PASSWORD = os.environ["SQL_DWBRICCS_PASSWORD"]
SQL_DWBRICCS_DATABASE = os.environ["SQL_DWBRICCS_DATABASE"]


class RedcapInstance(Enum):
    def internal():
        return {
            'staging_database': 'STG_redcap',
            'link_generator': get_redcap_link,
            'base_url': BASE_URL_INTERNAL,
        }

    def external():
        return {
            'staging_database': 'STG_redcap_briccsext',
            'link_generator': get_redcap_external_link,
            'base_url': BASE_URL_EXTERNAL,
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
