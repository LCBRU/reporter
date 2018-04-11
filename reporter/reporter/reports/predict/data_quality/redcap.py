#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import (
    RECIPIENT_PREDICT_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_PREDICT_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.data_quality import (
    RedcapInvalidStudyNumber,
    RedcapInvalidNhsNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidDate,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
)
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingData,
)
from reporter.reports.redcap.data_quality import (
    RedcapXrefMismatch,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)


CRF_PROJECT_ID = 62
DEMOGRAPHICS_PROJECT_ID = 63
REDCAP_INSTANCE = RedcapInstance.internal


# All

class PredictRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            study_name='Predict',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class PredictRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='Predict',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# CRF Validation

class PredictRedcapCrfMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=[
                'patient_id',
                'date_of_visit',
                'consent_date',
                'dob',
                'age_years',
                'gender',
                'height_cm',
                'weight_kg',
                'bmi_kg_m2',
                'hip_circumference_cm',
                'waist_circumference_cm',
                'smoker',
                'ethnicity',
                'sbp1_mmhg',
                'sbp2_mmhg',
                'sbp3_mmhg',
                'avg_sbp_mmhg',
                'dbp1_mmhg',
                'dbp2_mmhg',
                'dbp3_mmhg',
                'avg_dbp_mmhg',
                'hr1_bpm',
                'hr2_bpm',
                'hr3_bpm',
                'avg_hr_bpm',
            ],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidPatientId(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['patient_id'],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidDates(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            systolic_field_name='sbp1_mmhg',
            diastolic_field_name='dbp1_mmhg',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            systolic_field_name='sbp2_mmhg',
            diastolic_field_name='dbp2_mmhg',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            systolic_field_name='sbp3_mmhg',
            diastolic_field_name='dbp3_mmhg',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            systolic_field_name='avg_sbp_mmhg',
            diastolic_field_name='avg_dbp_mmhg',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['hr1_bpm', 'hr2_bpm', 'hr3_bpm', 'avg_hr_bpm'],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['height_cm'],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['weight_kg'],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['bmi_kg_m2'],
            recipients=[RECIPIENT_ADMIN],
        )


# Demographics Validation

class PredictRedcapDemographicsMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=[
                'patient_id',
                'research_appt_date',
                'nhs_no',
                's_no',
                'first_name',
                'last_name',
                'dob',
                'add_1',
                'postcode',
                'gender',
                'ethnicity',
                'gp_name',
                'gp_address_line_1',
                'gp_postcode',
            ],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapDemographicsInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['nhs_no'],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapDemographicsInvalidDates(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapDemographicsInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['s_no'],
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapDemographicsInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['postcode', 'gp_postcode'],
            recipients=[RECIPIENT_ADMIN],
        )


# CRF / Demographics XRef Validation

class PredictRedcapXrefMismatchPatientId(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=REDCAP_INSTANCE,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='patient_id',
            redcap_instance_b=REDCAP_INSTANCE,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='patient_id',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapXrefMismatchDob(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=REDCAP_INSTANCE,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='dob',
            redcap_instance_b=REDCAP_INSTANCE,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='dob',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapXrefMismatchGender(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=REDCAP_INSTANCE,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='gender',
            redcap_instance_b=REDCAP_INSTANCE,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='gender',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapXrefMismatchEthnicity(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=REDCAP_INSTANCE,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='ethnicity',
            redcap_instance_b=REDCAP_INSTANCE,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='ethnicity',
            recipients=[RECIPIENT_ADMIN],
        )


class PredictRedcapCrfWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class PredictRedcapDemographicsWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            DEMOGRAPHICS_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
