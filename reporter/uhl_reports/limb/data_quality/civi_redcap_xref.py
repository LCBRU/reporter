#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
    RedcapNotInCiviCrm,
)
from reporter.connections import RedcapInstance

CASE_TYPE_ID = 28
LIMB_REDCAP_PROJECT_ID = 32


class LimbCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[LIMB_REDCAP_PROJECT_ID],
            redcap_instance=RedcapInstance.uol_lamp(),
        )


class LimbRedcapNotInCiviCrm(RedcapNotInCiviCrm):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[LIMB_REDCAP_PROJECT_ID],
            redcap_instance=RedcapInstance.uol_lamp(),
        )
