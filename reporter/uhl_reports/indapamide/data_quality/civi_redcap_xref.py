#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)
from reporter.core import Schedule

CASE_TYPE_ID = 19
INDAPAMIDE_REDCAP_PROJECT_ID = 50


class IndapamideCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[INDAPAMIDE_REDCAP_PROJECT_ID],
            schedule=Schedule.never,
        )


class IndapamideRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[INDAPAMIDE_REDCAP_PROJECT_ID],
            schedule=Schedule.never,
        )
