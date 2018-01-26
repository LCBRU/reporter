#!/usr/bin/env python3

from reporter.reports import SqlReport, Schedule
from reporter.reports.redcap import get_redcap_link
from reporter.reports.emailing import (
    RECIPIENT_SCAD_MANAGER,
    RECIPIENT_SCAD_ADMIN,
)


class ScadRecruitedNotConsentedReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following SCAD participants are "
                          "recruited, but do not have full consent:"),
            recipients=[RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN],
            schedule=Schedule.weekly,
            sql='''

SELECT StudyNumber
FROM    i2b2_app03_scad_Data.dbo.LOAD_REDCap
WHERE FullConsent = 0

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}**\r\n".format(get_redcap_link(
                p['StudyNumber'], 28, p['StudyNumber']))

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1
