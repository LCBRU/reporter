#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    RECIPIENT_BRICCS_ADMIN, get_case_link)

# Abstract Reports


class DuplicateCiviCrmStudyIdReport(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants have "
                          "duplicated study IDs"),
            recipients=recipients,
            schedule=schedule,
            sql='''
SELECT
    StudyNumber,
    civicrm_contact_id,
    civicrm_case_id
FROM    {0}.dbo.LOAD_Civicrm
WHERE StudyNumber IN (
    SELECT a.StudyNumber
    FROM {0}.dbo.LOAD_Civicrm a
    WHERE a.blank_study_id = 0
    GROUP BY a.StudyNumber
    HAVING COUNT(*) > 1
)
ORDER BY StudyNumber
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['StudyNumber'],
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))

# BRICCS


class BriccsCiviCrmDuplicateStudyIdReport(
        DuplicateCiviCrmStudyIdReport):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            recipients=[RECIPIENT_BRICCS_ADMIN],
            schedule=Schedule.daily)
