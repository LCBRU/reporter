#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.uhl_reports.civicrm import get_case_link
from reporter.uhl_reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
from reporter.uhl_reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
    MissingNhsNumber,
    MissingDateOfBirth,
    MissingRecruitmentDate,
    MissingSampleFetchedDate,
    InvalidGender,
)
from reporter.uhl_reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
)
from reporter.emailing import (
    RECIPIENT_GENVASC_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_IT_DWH,
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


class GenvascPatientSummaryMissingRecruited(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT
    a.CaseId,
    a.CiviCrmId
FROM i2b2_app03_genvasc_Data.[dbo].LOAD_ValidEnrollments a
WHERE NOT EXISTS (
        SELECT 1
        FROM i2b2_app03_genvasc_Data.[dbo].PatientSummary
        WHERE StudyNumber = a.StudyNumber
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["CaseId"],
                row["CiviCrmId"]))
