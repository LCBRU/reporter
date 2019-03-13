#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_EXTEND_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_EXTEND_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidBmi,
)

REDCAP_PROJECT_ID = 17


class ExtendMalawiRedcapRecordId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^EXT\d{4}--[12]$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapMeiruId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=['meiru_study_id'],
            regular_expression='^\d{7}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidHeightInCm(RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=[
                'base_height',
                'follow_up_height',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=[
                'base_weight',
                'follow_up_weight',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBmi(RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=[
                'base_bmi_calc',
                'follow_up_bmi_calc',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureBase1(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_systolic_1'],
            diastolic_field_name=['base_diastolic_1'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureBase2(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_systolic_2'],
            diastolic_field_name=['base_diastolic_2'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureBase3(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_systolic_3'],
            diastolic_field_name=['base_diastolic_3'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureBaseAvg(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_avg_systolic'],
            diastolic_field_name=['base_avg_diastolic'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureFollowUp1(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_systolic_1'],
            diastolic_field_name=['follow_up_diastolic_1'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureFollowUp2(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_systolic_2'],
            diastolic_field_name=['follow_up_diastolic_2'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureFollowUp3(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_systolic_3'],
            diastolic_field_name=['follow_up_diastolic_3'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidBloodPressureFollowUpAvg(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_avg_systolic'],
            diastolic_field_name=['follow_up_avg_diastolic'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMalawiRedcapInvalidPulse(RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=[
                'base_heart_rate_1',
                'base_heart_rate_2',
                'base_heart_rate_3',
                'base_avg_heart_rate',
                'follow_up_heart_rate_1',
                'follow_up_heart_rate_2',
                'follow_up_heart_rate_3',
                'follow_up_avg_heart_rate',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
