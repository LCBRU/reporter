#!/usr/bin/env python3

from reporter.reports import Report
from reporter.reports.civicrm import get_case_link, get_contact_link


class ValidEnrolmentsStudyIdDuplicates(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated study ids"),
            recipients=recipients,
            schedule=schedule,
            sql='''
        SELECT
            StudyNumber,
            CaseId,
            CiviCrmId
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
                row["CaseId"],
                row["CiviCrmId"]))


class ValidEnrolmentsContactMultipleRecruitments(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants have multiple "
                          "recruited enrolments"),
            recipients=recipients,
            schedule=schedule,
            sql='''
            SELECT CiviCrmId
            FROM {}.dbo.LOAD_ValidEnrollments
            GROUP BY CiviCrmId
            HAVING COUNT(*) > 1
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link('Click to View', row["CiviCrmId"]))
