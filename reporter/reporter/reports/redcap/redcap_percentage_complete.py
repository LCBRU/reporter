#!/usr/bin/env python3

import math
from itertools import groupby
from reporter.reports import SqlReport


class RedcapPercentageCompleteReport(SqlReport):
    def __init__(
            self,
            study_name,
            recipients,
            schedule=None):
        super().__init__(
            name="Redcap Percentage Complete Report ({})".format(study_name),
            introduction=("Percentage completeness of REDCap CRFs"
                          "for {} study".format(study_name)),
            recipients=recipients,
            sql='''
                SELECT project_id
                      ,UPPER(project_name) AS project_name
                      ,form_name
                      ,Completed
                      ,Total
                      ,PercentageComplete AS perc
                      , last_used
                FROM CIVICRM_ScheduledReports_REDCapFormPercentageComplete
                WHERE study = %s
                ORDER BY project_name, form_name
                ''',
            parameters=(study_name),
            schedule=schedule
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for project, forms in groupby(cursor, lambda r: (
            r['project_name'],
            r['last_used'])
        ):
            markdown += "**{}**\r\n\r\n".format(project[0])
            markdown += "_Last Used {::%d-%b-%Y}_:\r\n\r\n".format(project[1])

            for form in forms:
                markdown += "- **{}**: ".format(form['form_name'].title())
                markdown += "{}%\r\n\r\n".format(math.floor(form['perc']))

        return markdown, cursor.rowcount + 1

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['patient_num'])
