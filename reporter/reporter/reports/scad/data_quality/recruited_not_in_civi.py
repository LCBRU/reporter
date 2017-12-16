#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.redcap import get_redcap_link
from reporter.reports.emailing import RECIPIENT_IT_DQ


class ScadRecruitedNotInCivicrm(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following SCAD participants are "
                          "recruited, but are not in civicrm:"),
            recipients=[RECIPIENT_IT_DQ],
            schedule=Schedule.weekly,
            sql='''

SELECT rc.[StudyNumber]
FROM [i2b2_app03_scad_Data].[dbo].[LOAD_REDCap] rc
WHERE NOT EXISTS (
    SELECT 1
    FROM    i2b2_app03_scad_Data.dbo.LOAD_CiviCRM cv
    WHERE cv.StudyNumber = rc.StudyNumber
)

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}**\r\n".format(get_redcap_link(
                p['StudyNumber'], 28, p['StudyNumber']))

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1
