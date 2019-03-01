#!/usr/bin/env python3

from reporter.core import Schedule
from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 5
GRAPHIC2_REDCAP_PROJECT_ID = 20


class Graphic2ivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            redcap_project_id=GRAPHIC2_REDCAP_PROJECT_ID,
            schedule=Schedule.never,
        )


class Graphic2RedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            project_id=GRAPHIC2_REDCAP_PROJECT_ID,
            schedule=Schedule.never,
        )
