#!/usr/bin/env python3

import re
from reporter.core import SqlReport
from reporter.connections import RedcapInstance
from reporter.connections import DatabaseConnection
from reporter.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRAVE_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapInvalidNhsNumber,
)


REDCAP_PROJECT_ID = 25

# Abstract Reports


class FoamiRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['nhs_num'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
