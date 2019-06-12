#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_LIMB_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_LIMB_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
)

REDCAP_PROJECT_ID = 32


class LimbRedcapStudyNumber(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^[A-Z]{2}\d{4}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBmi(RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
