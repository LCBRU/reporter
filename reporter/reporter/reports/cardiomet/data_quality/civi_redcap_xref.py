#!/usr/bin/env python3

from reporter.reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 24
PROJECT_ID = 67


class CardiometCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            project_id=PROJECT_ID
        )


class CardiometRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            project_id=PROJECT_ID
        )
