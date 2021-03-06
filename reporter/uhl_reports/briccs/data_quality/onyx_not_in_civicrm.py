#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_IT_DWH


class BriccsInOnyxNotInCiviCrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following Glenfield participants are "
                          "in Onyx, but are not in CiviCrm"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''

SELECT StudyNumber
FROM [i2b2_app03_b1_data].[dbo].[LOAD_Onyx] o
WHERE NOT EXISTS (
    SELECT 1
    FROM    i2b2_app03_b1_data.dbo.LOAD_Civicrm
    WHERE StudyNumber = o.StudyNumber
) AND RecruitingSite = 'briccs_glenfield_recruitment'

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(row["StudyNumber"])
