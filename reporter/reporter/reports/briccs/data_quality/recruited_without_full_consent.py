#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_contact_id_search_link, RECIPIENT_BRICCS_ADMIN


class BriccsRecruitedWithoutFullConsent(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are recruited "
                          "or duplicates in CiviCRM, but a "
                          "record of full consent cannot be found"),
            recipients=[RECIPIENT_BRICCS_ADMIN],
            schedule=Schedule.never,
            sql='''

SELECT
    b.StudyNumber,
    b.consent_date
FROM    i2b2_app03_b1_Data.dbo.LOAD_Civicrm b
WHERE
        b.blank_study_id = 0
    AND b.is_recruited = 1
    AND NOT EXISTS (
        SELECT 1
        FROM i2b2_app03_b1_Data.dbo.Load_Fully_Consented
        WHERE StudyNumber = b.StudyNumber
    )

                '''
        )

    def get_report_line(self, row):
        consent_date = ('{:%d-%b-%Y}'.format(row["consent_date"])
                        if row['consent_date'] else '')
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row["StudyNumber"],
                row["StudyNumber"]),
            consent_date)
