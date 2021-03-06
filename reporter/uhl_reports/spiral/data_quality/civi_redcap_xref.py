#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)
from reporter.core import Schedule

CASE_TYPE_ID = 25
SPIRAL_REDCAP_PROJECT_ID = 69


class SpiralCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[SPIRAL_REDCAP_PROJECT_ID],
            schedule=Schedule.never,
        )


class SpiralRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[SPIRAL_REDCAP_PROJECT_ID],
            schedule=Schedule.never,
        )
