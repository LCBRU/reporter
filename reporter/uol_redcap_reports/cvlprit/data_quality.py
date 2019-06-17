#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_CVLPRIT_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_CVLPRIT_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInM,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidBloodPressure,
)

REDCAP_PROJECT_ID = 18


class CvlpritRedcapRecordId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^\d{1,4}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class CvlpritRedcapGlobalPatientId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['patient_id'],
            regular_expression='^X\d{3}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class CvlpritRedcapLocalSitePatientId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['local_id'],
            regular_expression='\d{1,3}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class CvlpritRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class CvlpritRedcapInvalidHeightInM(RedcapInvalidHeightInM):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class CvlpritRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class CvlpritRedcapInvalidBloodPressure(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['systolic_bp'],
            diastolic_field_name=['diastolic_bp'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
