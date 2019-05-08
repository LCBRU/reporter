#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    RedcapNotInCiviCrm,
)

CASE_TYPE_ID = 6
PROJECT_ID = 53


class MinervaRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[PROJECT_ID],
        )
