#!/usr/bin/env python3

from reporter.reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
from reporter.reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
    MissingNhsNumber,
    MissingDateOfBirth,
    MissingRecruitmentDate,
    MissingSampleFetchedDate,
    InvalidGender,
)
from reporter.reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
)
from reporter.reports.emailing import (
    RECIPIENT_GENVASC_ADMIN as RECIPIENT_ADMIN,
)


I2B2_DB = "i2b2_app03_genvasc_Data"


class GenvascPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class GenvascPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class GenvascPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class GenvascPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'StudyNumber',
                'RecruitmentDate',
                'Gender',
                'HeightAtRecruitment',
                'WeightAtRecruitment',
                'Ethnicity',
                'ConsentDate',
            ]
        )


class GenavscPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)


class GenvascMissingNhsNumber(
        MissingNhsNumber):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN])


class GenvascMissingDateOfBirth(
        MissingDateOfBirth):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN])


class GenvascMissingRecruitmentDate(
        MissingRecruitmentDate):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN])


class GenvascMissingSampleFetchedDate(
        MissingSampleFetchedDate):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN])


class GenvascInvalidGender(
        InvalidGender):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN])


class GenvascValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class GenvascValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )
