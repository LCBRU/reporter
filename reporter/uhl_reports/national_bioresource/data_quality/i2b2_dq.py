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
)
from reporter.uhl_reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
    RecruitedWithoutFullConsent,
)
from reporter.emailing import (
    RECIPIENT_BIORESOURCE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_IT_DWH,
)
from reporter.connections import get_redcap_link


I2B2_DB = "i2b2_app03_national_bioresource_Data"
REDCAP_PROJECT_ID = 9


class NationalBioresourcePatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class NationalBioresourcePatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class NationalBioresourcePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class NationalBioresourcePatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'NhsNumber',
                'UhlSystemNumber',
                'StudyNumber',
                'NationalBioresourceId',
                'consent_date',
                'DateOfBirth',
                'gender',
                'ethnicity',
            ]
        )

    def get_report_line(self, row):
        missing_fields = [f for f in self.fields if row[f] == 1]

        return '- {}: ({})\r\n'.format(
            get_redcap_link(
                row['ID'],
                REDCAP_PROJECT_ID,
                row['ID'],
            ),
            ', '.join(missing_fields),
        )


class NationalBioresourcePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)


class NationalBioresourceValidEnrolmentsStudyIdDuplicates(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated study ids"),
            recipients=[RECIPIENT_ADMIN],
            schedule=None,
            sql='''
        SELECT
            StudyNumber,
            civicrm_case_id,
            civicrm_contact_id
        FROM {0}.dbo.Cache_LOAD_ValidEnrollments
        WHERE StudyNumber IN (
            SELECT StudyNumber
            FROM {0}.dbo.Cache_LOAD_ValidEnrollments
            GROUP BY StudyNumber
            HAVING COUNT(*) > 1
        )
        ORDER BY StudyNumber
                '''.format(I2B2_DB)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['StudyNumber'],
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))


class NationalBioresourceValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class NationalBioresourcePatientSummaryMissingRecruited(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  civicrm_case_id, civicrm_contact_id
FROM [i2b2_app03_National_BioResource_Data].[dbo].[LOAD_Civicrm_Bioresource] a
JOIN [i2b2_app03_National_BioResource_Data].[dbo].[LOAD_FullyConsented] fc
	ON fc.StudyNumber = a.national_bioresource_id
WHERE NOT EXISTS (
        SELECT 1
        FROM [i2b2_app03_National_BioResource_Data].[dbo].PatientSummary
        WHERE StudyNumber = a.national_bioresource_id
)

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))


class NationalBioresourceRecruitedWithoutFullConsent(
        RecruitedWithoutFullConsent):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )
