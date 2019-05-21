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
)
from reporter.emailing import (
    RECIPIENT_TMAO_ADMIN as RECIPIENT_ADMIN,
)
from reporter.core import Schedule


I2B2_DB = "i2b2_app03_tmao_Data"


class TmaoPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class TmaoPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class TmaoatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class TmaoPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'CiviCrmCaseId',
                'UhlSystemNumber',
                'StudyNumber',
                'Gender',
                'DateOfBirth',
            ],
            schedule=Schedule.never,
        )


class TmaoPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            schedule=Schedule.never,
        )


class TmaoValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )
