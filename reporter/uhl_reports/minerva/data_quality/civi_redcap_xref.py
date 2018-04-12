#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 6
PROJECT_ID = 53


class MinervaRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            project_id=PROJECT_ID
        )
