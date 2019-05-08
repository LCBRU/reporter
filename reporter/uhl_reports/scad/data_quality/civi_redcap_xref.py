#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 9
SCAD_REDCAP_PROJECT_ID = 28
SCAD_REDCAP_PROJECT_ID_V2 = 77


class ScadCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[SCAD_REDCAP_PROJECT_ID, SCAD_REDCAP_PROJECT_ID_V2],
        )


class ScadRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[SCAD_REDCAP_PROJECT_ID],
        )
