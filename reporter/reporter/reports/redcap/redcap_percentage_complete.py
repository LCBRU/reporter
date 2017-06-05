#!/usr/bin/env python3

import math
from itertools import groupby
from reporter.reports import Report
from reporter import (
    RECIPIENT_BIORESOURCE_MANAGER, RECIPIENT_BIORESOURCE_ADMIN,
    RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCS_ADMIN,
    RECIPIENT_AS_MANAGER, RECIPIENT_AS_ADMIN,
    RECIPIENT_BRAVE_MANAGER, RECIPIENT_BRAVE_ADMIN,
    RECIPIENT_DREAM_MANAGER, RECIPIENT_DREAM_ADMIN,
    RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN,
    RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN)


class RedcapPercentageCompleteReport(Report):
    def __init__(self, study_name, recipients):
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
            parameters=(study_name)
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


class AsRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'AS',
            [RECIPIENT_AS_ADMIN, RECIPIENT_AS_MANAGER])


class BioresRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Bioresource',
            [RECIPIENT_BIORESOURCE_MANAGER, RECIPIENT_BIORESOURCE_ADMIN])


class BraveRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [RECIPIENT_BRAVE_ADMIN, RECIPIENT_BRAVE_MANAGER])


class BriccsRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'BRICCS',
            [RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCS_ADMIN])


class DreamRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'DREAM',
            [RECIPIENT_DREAM_MANAGER, RECIPIENT_DREAM_ADMIN])


class ScadRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'SCAD',
            [RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN])


class TmaoRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'TMAO',
            [RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN])
