#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 23
PREDICT_REDCAP_PROJECT_ID = 62


class PredictCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[PREDICT_REDCAP_PROJECT_ID],
        )


class PredictRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[PREDICT_REDCAP_PROJECT_ID],
        )
