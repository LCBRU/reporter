#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_BRICCS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRICCS_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapInvalidNhsNumber,
    RedcapInvalidDate,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
    RedcapInvalidEmailAddress,
    RedcapFieldMatchesRegularExpression,
    RedcapMissingDataWhen,
    RedcapMissingData,
)

REDCAP_LEICESTER_PROJECT_ID = 24
REDCAP_DONCASTER_PROJECT_ID = 13
REDCAP_SHEFFIELD_PROJECT_ID = 14
REDCAP_KETTERING_PROJECT_ID = 15
REDCAP_CHESTERFIELD_PROJECT_ID = 16
REDCAP_GRANTHAM_PROJECT_ID = 17
REDCAP_LINCOLN_PROJECT_ID = 18
REDCAP_NORTHAMPTON_PROJECT_ID = 19
REDCAP_DERBY_PROJECT_ID = 25
REDCAP_BOSTON_PROJECT_ID = 26
REDCAP_NOTTINGHAM_PROJECT_ID = 27

# All


class BriccsRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            study_name='BRICCS',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='BRICCS',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )

# Leicester


class BriccsLeicesterRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsLeicesterRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
                'urine_sample',
            ],
            regular_expression='^(|BSa\d{8}|BSa00\d{8})$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsLeicesterRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLeicesterRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Doncaster


class BriccsDoncasterRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsDoncasterBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsDoncasterRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsDoncasterRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDoncasterRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DONCASTER_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Sheffield


class BriccsSheffieldRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsSheffieldBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsSheffieldRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsSheffieldRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsSheffieldRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Kettering


class BriccsKetteringRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsKetteringBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsKetteringRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsKetteringRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsKetteringRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Chesterfield


class BriccsChesterfieldRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsChesterfieldBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsChesterfieldRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsChesterfieldRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsChesterfieldRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_CHESTERFIELD_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Grantham


class BriccsGranthamRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsGranthamBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
)


class BriccsGranthamRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsGranthamRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsGranthamRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Lincoln


class BriccsLincolnRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsLincolnBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsLincolnRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsLincolnRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsLincolnRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Northampton


class BriccsNorthamptonRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsNorthamptonBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsNorthamptonRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsNorthamptonRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNorthamptonRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NORTHAMPTON_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Derby


class BriccsDerbyRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsDerbyBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsDerbyRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsDerbyRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsDerbyRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_DERBY_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Boston


class BriccsBostonRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsBostonBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsBostonRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsBostonRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsBostonRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_BOSTON_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Nottingham


class BriccsNottinghamRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BriccsNottinghamBmiMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['part_bmi'],
            indicator_field='criteria_met',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamHeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['part_height'],
            indicator_field='epi_obs_height_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamWeightMissing(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['part_weight'],
            indicator_field='epi_obs_weight_yn',
            indicator_value='1',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['record_id'],
            regular_expression='BPt\d{8}',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsNottinghamRedcapInvalidSampleNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=[
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            regular_expression='(|BSa\d{8})',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            ignore_case=True,
        )


class BriccsNottinghamRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BriccsNottinghamRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_NOTTINGHAM_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
