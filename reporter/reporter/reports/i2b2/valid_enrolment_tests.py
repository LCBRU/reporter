#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.reports.civicrm import get_case_link, get_contact_link
from reporter.reports.civicrm import (
    get_contact_id_search_link,
)


class ValidEnrolmentsStudyIdDuplicates(SqlReport):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated study ids"),
            recipients=recipients,
            schedule=schedule,
            sql='''
        SELECT
            StudyNumber,
            civicrm_case_id,
            civicrm_contact_id
        FROM {0}.dbo.LOAD_ValidEnrollments
        WHERE StudyNumber IN (
            SELECT StudyNumber
            FROM {0}.dbo.LOAD_ValidEnrollments
            GROUP BY StudyNumber
            HAVING COUNT(*) > 1
        )
        ORDER BY StudyNumber
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['StudyNumber'],
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))


class ValidEnrolmentsContactMultipleRecruitments(SqlReport):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants have multiple "
                          "recruited enrolments"),
            recipients=recipients,
            schedule=schedule,
            sql='''
            SELECT civicrm_contact_id
            FROM {}.dbo.LOAD_ValidEnrollments
            GROUP BY civicrm_contact_id
            HAVING COUNT(*) > 1
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link('Click to View', row["civicrm_contact_id"]))


class RecruitedWithoutFullConsent(SqlReport):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants are recruited "
                          "or duplicates in CiviCRM, but a "
                          "record of full consent cannot be found"),
            recipients=recipients,
            schedule=schedule,
            sql='''

            SELECT  StudyNumber
            FROM    {0}.dbo.LOAD_Civicrm rec
            WHERE NOT EXISTS (
                SELECT 1
                FROM    {0}.[dbo].[LOAD_FullyConsented]
                WHERE StudyNumber = rec.StudyNumber
            )
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row['StudyNumber'],
                row['StudyNumber']))


class PatientSummaryMissingRecruited(SqlReport):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants have an error "
                          "so they have not reached the i2b2 patient summary"),
            recipients=recipients,
            schedule=schedule,
            sql='''

                SELECT
                    StudyNumber,
                    civicrm_case_id,
                    civicrm_contact_id
                FROM {0}.[dbo].LOAD_Civicrm a
                WHERE is_recruited = 1
                    AND NOT EXISTS (
                        SELECT 1
                        FROM {0}.[dbo].PatientSummary
                        WHERE StudyNumber = a.StudyNumber
                    )
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row["StudyNumber"] or 'Click to View',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))
