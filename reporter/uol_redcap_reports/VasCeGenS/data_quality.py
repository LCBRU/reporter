#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_VASCEGENS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_VASCEGENS_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInM,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidBloodPressure,
)

REDCAP_PROJECT_ID = 19


class VasCeGenSRedcapRecordId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^UMB-\d{4}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class VasCeGenSRedcapAnthonyNolanReference(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['anthony_nolan_ref'],
            regular_expression='^G\d{12}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class VasCeGenSRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
