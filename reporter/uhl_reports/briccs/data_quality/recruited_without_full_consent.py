#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_BRICCS_ADMIN
from reporter.uhl_reports.civicrm import (
    get_contact_id_search_link,
)


class BriccsRecruitedWithoutFullConsent(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are recruited "
                          "or duplicates in CiviCRM, but a "
                          "record of full consent cannot be found"),
            recipients=[RECIPIENT_BRICCS_ADMIN],
            sql='''

SELECT
    StudyNumber,
    Source
FROM    i2b2_app03_b1_data.[dbo].[LOAD_ALL_Recruited] ar
WHERE NOT EXISTS (
    SELECT 1
    FROM    i2b2_app03_b1_data.[dbo].[LOAD_Fully_Consented]
    WHERE StudyNumber = ar.StudyNumber
) AND LEN(RTRIM(LTRIM(COALESCE(StudyNumber, '')))) > 0

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row['StudyNumber'],
                row['StudyNumber']))
