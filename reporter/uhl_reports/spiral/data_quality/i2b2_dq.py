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
    RECIPIENT_SPIRAL_ADMIN as RECIPIENT_ADMIN,
)
from reporter.core import Schedule


I2B2_DB = "i2b2_app03_spiral_Data"


class SpiralPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class SpiralPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class SpiralPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class SpiralPatientSummaryMissingData(
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


class SpiralPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class SpiralValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class SpiralValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class SpiralRecruitedWithoutFullConsent(
        RecruitedWithoutFullConsent):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class SpiralPatientSummaryMissingRecruited(
        PatientSummaryMissingRecruited):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )
