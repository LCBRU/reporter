#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_PREECLAMPSIA_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_PREECLAMPSIA_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapInvalidStudyNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidDate,
    RedcapInvalidUhlSystemNumber,
)
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.core import Schedule


PROJECT_ID = 39
REDCAP_INSTANCE = RedcapInstance.internal


# All

class PreeclampsiaRedcapPercentageCompleteReport(
    RedcapPercentageCompleteReport
):
    def __init__(self):
        super().__init__(
            study_name='Preeclampsia',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='Preeclampsia',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


# CRF Validation

class PreeclampsiaRedcapInvalidPatientId(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            fields=['patient_id'],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidDates(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            systolic_field_name='systolic',
            diastolic_field_name='diastolic',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            systolic_field_name='nicom_systolic',
            diastolic_field_name='nicom_diastolic',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            fields=['nicom_pulse', 'pulse'],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            fields=['maternal_height'],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            fields=['maternal_weight'],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            fields=['bmi'],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )
