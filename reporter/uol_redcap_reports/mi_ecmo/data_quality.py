#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_MI_ECMO_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_MI_ECMO_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
)

REDCAP_PROJECT_ID = 14


class MiEcmoRedcapStudyNumber(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^\d{3}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MiEcmoRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MiEcmoRedcapInvalidHeightInCm(RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MiEcmoRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
