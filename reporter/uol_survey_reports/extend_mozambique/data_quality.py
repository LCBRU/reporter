#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_EXTEND_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_EXTEND_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInM,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidBmi,
)

REDCAP_PROJECT_ID = 21


class ExtendMozambiqueRedcapRecordId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^\d{1,4}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapMeiruId(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            fields=['meiru_study_id'],
            regular_expression='^\d{7}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidHeightInM(RedcapInvalidHeightInM):
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


class ExtendMozambiqueRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
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


class ExtendMozambiqueRedcapInvalidBmi(RedcapInvalidBmi):
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


class ExtendMozambiqueRedcapInvalidBloodPressureBase1(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_systolic_1'],
            diastolic_field_name=['base_diastolic_1'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureBase2(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_systolic_2'],
            diastolic_field_name=['base_diastolic_2'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureBase3(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_systolic_3'],
            diastolic_field_name=['base_diastolic_3'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureBaseAvg(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['base_avg_systolic'],
            diastolic_field_name=['base_avg_diastolic'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureFollowUp1(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_systolic_1'],
            diastolic_field_name=['follow_up_diastolic_1'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureFollowUp2(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_systolic_2'],
            diastolic_field_name=['follow_up_diastolic_2'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureFollowUp3(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_systolic_3'],
            diastolic_field_name=['follow_up_diastolic_3'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidBloodPressureFollowUpAvg(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_survey,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name=['follow_up_avg_systolic'],
            diastolic_field_name=['follow_up_avg_diastolic'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ExtendMozambiqueRedcapInvalidPulse(RedcapInvalidPulse):
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
