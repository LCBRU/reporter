#!/usr/bin/env python3

from reporter.reports import Report
from reporter import get_case_link, RECIPIENT_BIORESOURCE_ADMIN


class BioresourceIdDuplicates(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated bioresource ids"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''
        SELECT
            StudyNumber,
            legacy_bioresource_id,
            CaseId,
            CiviCrmId
        FROM i2b2_app03_bioresource_Data.dbo.LOAD_ValidEnrollments
        WHERE StudyNumber IN (
            SELECT StudyNumber
            FROM i2b2_app03_bioresource_Data.dbo.LOAD_ValidEnrollments
            GROUP BY StudyNumber
            HAVING COUNT(*) > 1
        )
        ORDER BY StudyNumber
                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['StudyNumber'],
                row["CaseId"],
                row["CiviCrmId"]))
