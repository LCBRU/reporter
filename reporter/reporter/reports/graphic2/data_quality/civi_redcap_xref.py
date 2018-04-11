#!/usr/bin/env python3

from reporter.core import Schedule
from reporter.reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 5
PROJECT_ID = 20


class Graphic2ivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            project_id=PROJECT_ID,
            schedule=Schedule.never,
        )


class Graphic2RedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            project_id=PROJECT_ID,
            schedule=Schedule.never,
        )
