import schedule
import logging
from reporter import (send_markdown_email, send_markdown_slack,
                      get_report_db, get_dwbriccs_db,
                      get_contact_id_search_link)


class Report:
    def __init__(self, sql, introduction=None, recipients=None,
                 name=None, conn=None, parameters=None):

        self.sql = sql
        self.name = name or type(self).__name__
        self.conn = conn or get_report_db()
        self.recipients = recipients or ('DEFAULT_RECIPIENT')
        self.introduction = introduction or ''
        self.parameters = parameters or ()

    def schedule(self):
        schedule.every().monday.at("08:00").do(self.run)
        logging.info("{} scheduled".format(self.name))

    def run(self):
        report, rows, attachments = self.get_report()

        logging.info("{} ran with {} rows".format(self.name, rows))

        if (rows == 0):
            return

        send_markdown_email(
            self.name,
            self.recipients,
            report,
            attachments)

        if attachments is None:
            send_markdown_slack(self.name, report)

    def get_report(self):
        attachments = None

        with self.conn as conn:

            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(self.sql, self.parameters)

                if cursor.rowcount == 0:
                    return None, 0, attachments

                report, rows = self.get_report_lines(cursor)

        markdown = "**{}**\r\n\r\n".format(self.name)
        markdown += "_{}_:\r\n\r\n".format(self.introduction)
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
    def __init__(self, project, recipients):
        super().__init__(
            introduction=('The following participant details do not match '
                          'the details in the UHL PMI'),
            conn=get_dwbriccs_db(),
            recipients=recipients,
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
                parameters=(project)
        )

    def get_report_line(self, row):
        errors = []

        if row["system_number_missing"] == 1:
            errors.append('UHL System number not found')

        if row["nhs_number_mismatch"] == 1:
            errors.append(
                'NHS Number mismatch (Study=\'{}\'; PMI=\'{}\''.format(
                    row['study_nhs_number'],
                    row['pmi_nhs_number']))

        if row["date_of_birth_mismatch"] == 1:
            errors.append(
                'DOB mismatch (Study=\'{}\'; PMI=\'{}\''.format(
                    row['study_date_of_birth'],
                    row['pmi_date_of_birth']))

        return '- {}): {}\n'.format(
            get_contact_id_search_link(row["StudyID"], row["StudyID"]),
            '; '.join(errors)
        )


from reporter.reports.bioresource import *
from reporter.reports.genvasc import *
from reporter.reports.graphic2 import *
from reporter.reports.redcap import *
