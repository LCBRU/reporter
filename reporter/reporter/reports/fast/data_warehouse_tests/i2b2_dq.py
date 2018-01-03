#!/usr/bin/env python3

from reporter.reports import Report
from reporter.reports.civicrm import get_case_link
from reporter.reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
from reporter.reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
)
from reporter.reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
)
from reporter.reports.emailing import (
    RECIPIENT_FAST_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_IT_DWH,
)


I2B2_DB = "i2b2_app03_fast_Data"


class FastPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class FastPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class FastPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class FastPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'NhsNumber',
                'StudyNumber',
                'CiviCrmId',
                'consent_date',
                'gender',
            ]
        )


class FastPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)


class FastValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class FastValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class FastPatientSummaryMissingRecruited(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  StudyNumber, civicrm_case_id, civicrm_contact_id
FROM [i2b2_app03_fast_Data].[dbo].LOAD_Civicrm a
WHERE is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM [i2b2_app03_fast_Data].[dbo].PatientSummary
        WHERE StudyNumber = a.StudyNumber
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row["StudyNumber"] or 'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))
