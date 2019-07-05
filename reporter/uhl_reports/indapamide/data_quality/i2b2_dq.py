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
    RECIPIENT_INDAPAMIDE_ADMIN as RECIPIENT_ADMIN,
)
from reporter.core import Schedule


I2B2_DB = "i2b2_app03_indapamide_Data"


class IndapamidePatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class IndapamidePatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class IndapamidePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class IndapamidePatientSummaryMissingData(
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
                'consent_date',
                'Gender',
                'DateOfBirth',
                'Ethnicity',
            ],
            schedule=Schedule.never,
        )


class IndapamidePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class IndapamideValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class IndapamideValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class IndapamideRecruitedWithoutFullConsent(
        RecruitedWithoutFullConsent):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class IndapamidePatientSummaryMissingRecruited(
        PatientSummaryMissingRecruited):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )
