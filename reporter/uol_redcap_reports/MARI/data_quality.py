#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_MARI_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_MARI_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidBloodPressure,
)

REDCAP_PROJECT_ID = 16


class MariRedcapStudyNumber(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^\d{1,3}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MariRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MariRedcapInvalidHeightInCm(RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['base_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MariRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['base_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MariRedcapInvalidBloodPressureBase(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_syst_bp'],
            diastolic_field_name=['base_diast_bp'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MariRedcapInvalidBloodPressureEndOfProcedure(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['systolic_bp_end_proc'],
            diastolic_field_name=['diastolic_bp_end_proc'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
