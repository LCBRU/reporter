#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
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
from reporter.core import Schedule

I2B2_DB = "i2b2_app03_bioresource_Data"
REDCAP_PROJECT_ID = 9


class BioresourcePatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            schedule=Schedule.never,
        )


class BioresourcePatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourcePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourcePatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'NhsNumber',
                'UhlSystemNumber',
                'BioresourceId',
                'StudyNumber',
                'EnrolmentDate',
                'ConsentDate',
                'Gender',
                'DOB',
                'DateOfBirth',
                'Height',
                'Weight',
            ],
            schedule=Schedule.never,
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


class BioresourcePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourceValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class BioresourceValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class BioresourcePatientSummaryMissingRecruited(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached i2b2"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT  civicrm_case_id, civicrm_contact_id
FROM [i2b2_app03_bioresource_Data].[dbo].[LOAD_Civicrm_Bioresource] a
WHERE is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM [i2b2_app03_bioresource_Data].[dbo].PatientSummary
        WHERE StudyNumber = a.bioresource_id
)

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))


class BioresourceRecruitedWithoutFullConsent(
        RecruitedWithoutFullConsent):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )
