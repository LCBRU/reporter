#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import (
    RECIPIENT_SPIRAL_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_SPIRAL_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.uhl_reports.redcap.data_quality import (
    RedcapInvalidStudyNumber,
    RedcapInvalidNhsNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidDate,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
    RedcapInvalidEmailAddress,
    RedcapXrefMismatch,
)
from reporter.uhl_reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.uhl_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.uhl_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)


DEMOGRAPHICS_PROJECT_ID = 68
CRF_PROJECT_ID = 69
REDCAP_INSTANCE = RedcapInstance.internal


# All

class SpiralRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            study_name='Spiral',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class SpiralRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='Spiral',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# CRF Validation

class SpiralRedcapCrfInvalidPatientId(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['record_id'],
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapCrfRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapCrfInvalidDates(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapCrfInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            systolic_field_name='systolic',
            diastolic_field_name='diastolic',
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapCrfInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['height'],
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapCrfInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['weight'],
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapCrfInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=CRF_PROJECT_ID,
            fields=['bmi'],
            recipients=[RECIPIENT_ADMIN],
        )


# Demographics Validation

class SpiralRedcapDemographicsInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['nhs_no'],
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapDemographicsInvalidDates(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapDemographicsInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['s_no'],
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapDemographicsInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['postcode', 'gp_postcode'],
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapDemographicsInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=DEMOGRAPHICS_PROJECT_ID,
            fields=['email_add'],
            recipients=[RECIPIENT_ADMIN],
        )


# CRF / Demographics XRef Validation

class SpiralRedcapXrefMismatchPatientId(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=REDCAP_INSTANCE,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='record_id',
            redcap_instance_b=REDCAP_INSTANCE,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='patient_id',
            recipients=[RECIPIENT_ADMIN],
        )


class SpiralRedcapXrefMismatchDob(
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


class SpiralRedcapCrfWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class SpiralRedcapDemographicsWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            DEMOGRAPHICS_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
