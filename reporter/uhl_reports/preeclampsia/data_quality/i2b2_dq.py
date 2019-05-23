#!/usr/bin/env python3

from reporter.uhl_reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
from reporter.uhl_reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
)
from reporter.uhl_reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
    RecruitedWithoutFullConsent,
    PatientSummaryMissingRecruited,
)
from reporter.emailing import (
    RECIPIENT_PREECLAMPSIA_ADMIN as RECIPIENT_ADMIN,
)
from reporter.core import Schedule


I2B2_DB = "i2b2_app03_preeclampsia_Data"


class PreeclampsiaPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB, schedule=Schedule.never)


class PreeclampsiaPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB, schedule=Schedule.never)


class PreeclampsiaPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB, schedule=Schedule.never)


class PreeclampsiaPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'CiviCrmCaseId',
                'NhsNumber',
                'UhlSystemNumber',
                'StudyNumber',
                'Gender',
                'DateOfBirth',
                'Ethnicity',
            ],
            schedule=Schedule.never,
        )


class PreeclampsiaPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB, schedule=Schedule.never)


class PreeclampsiaValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaRecruitedWithoutFullConsent(
        RecruitedWithoutFullConsent):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaPatientSummaryMissingRecruited(
        PatientSummaryMissingRecruited):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )
