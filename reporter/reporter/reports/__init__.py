import schedule
import logging
import re
from datetime import date
from enum import Enum
from reporter import (send_markdown_email, send_markdown_slack,
                      DatabaseConnection,
                      get_contact_id_search_link)


class Schedule(Enum):
    def daily(func):
        schedule.every().day.at("08:00").do(func)

    def weekly(func):
        schedule.every().monday.at("08:00").do(func)

    def never(func):
        pass


class Report:
    def __init__(self, sql, introduction=None, recipients=None,
                 name=None, conn=None, parameters=None, send_email=True,
                 send_slack=True, schedule=None):

        self._sql = sql
        self._name = name or '{} ({:%d-%b-%Y})'.format(
            type(self).__name__, date.today())

        # Unpick CamelCase
        self._name = re.sub('([a-z])([A-Z])', r'\1 \2', self._name)

        self._conn = conn or DatabaseConnection.reporting
        self._recipients = recipients or ('DEFAULT_RECIPIENT')
        self._introduction = introduction or ''
        self._parameters = parameters or ()
        self._send_email = send_email
        self._send_slack = send_slack
        self._schedule = schedule or Schedule.weekly

    def schedule(self):

        self._schedule(self.run)
        logging.info("{} scheduled".format(self._name))

    def run(self):
        report, rows, attachments = self.get_report()

        logging.info("{} ran with {} rows".format(self._name, rows))

        if (rows == 0):
            return

        if self._send_email:
            send_markdown_email(
                self._name,
                self._recipients,
                report,
                attachments)

        if self._send_slack:
            send_markdown_slack(self._name, report)

    def get_report(self):
        attachments = None

        with self._conn() as conn:

            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(self._sql, self._parameters)

                if cursor.rowcount == 0:
                    return None, 0, attachments

                report, rows = self.get_report_lines(cursor)

        markdown = "**{}**\r\n\r\n".format(self._name)
        markdown += "_{}_:\r\n\r\n".format(self._introduction)
        markdown += report
        markdown += "\r\n\r\n{} Record(s) Found".format(rows)

        return markdown, rows, attachments

    def get_report_lines(self, cursor):
        markdown = ''

        for row in cursor:
            markdown += self.get_report_line(row)

        return markdown, cursor.rowcount + 1

    def get_report_line(self, row):
        return '- {}\r\n'.format(row)


class PmiPatientMismatch(Report):
    def __init__(self, project, recipients, schedule=None):
        super().__init__(
            introduction=('The following participant details do not match '
                          'the details in the UHL PMI'),
            conn=DatabaseConnection.dwbriccs,
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''
                SELECT [StudyID]
                      ,[pmi_system_number]
                      ,[study_system_number]
                      ,[pmi_date_of_birth]
                      ,[study_date_of_birth]
                      ,[pmi_nhs_number]
                      ,[study_nhs_number]
                      ,[ProjectId]
                      ,[nhs_number_mismatch]
                      ,[date_of_birth_mismatch]
                      ,[system_number_missing]
                  FROM [DWBRICCS].[dbo].[LCBRU_Reports_PMI_Mismatch]
                  WHERE [ProjectId] = %s
                ''',
                parameters=(project),
                send_slack=False
        )

    def get_report_line(self, row):
        errors = []

        if row["system_number_missing"] == 1:
            errors.append('UHL System number not found')

        if row["nhs_number_mismatch"] == 1:
            errors.append(
                'NHS Number mismatch (Study=\'{}\'; PMI=\'{}\')'.format(
                    row['study_nhs_number'],
                    row['pmi_nhs_number']))

        if row["date_of_birth_mismatch"] == 1:
            errors.append(
                'DOB mismatch (Study=\'{}\'; PMI=\'{}\')'.format(
                    row['study_date_of_birth'],
                    row['pmi_date_of_birth']))

        return '- {}: {}\n'.format(
            get_contact_id_search_link(row["StudyID"], row["StudyID"]),
            '; '.join(errors)
        )


from reporter.reports.bioresource import *
from reporter.reports.briccs import *
from reporter.reports.genvasc import *
from reporter.reports.graphic2 import *
from reporter.reports.omics import *
from reporter.reports.redcap import *
from reporter.reports.civicrm import *
from reporter.reports.i2b2 import *
