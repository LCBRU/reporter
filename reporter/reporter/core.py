import schedule
import logging
import re
import datetime
import io
from datetime import date
from enum import Enum
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from reporter.reports.emailing import send_markdown_email
from reporter.reports.databases import DatabaseConnection


class Schedule(Enum):
    def daily(func):
        schedule.every().day.at("08:00").do(func)

    def weekly(func):
        schedule.every().monday.at("08:00").do(func)

    def monthly(func):
        schedule.every(4).weeks.do(func)

    def never(func):
        pass


class Report:
    def __init__(self, introduction=None, recipients=None,
                 name=None, send_email=True, schedule=None):

        self._name = name or type(self).__name__

        # Unpick CamelCase
        self._name = re.sub('([a-z])([A-Z])', r'\1 \2', self._name)

        self._recipients = recipients or ('DEFAULT_RECIPIENT')
        self._introduction = introduction or ''
        self._send_email = send_email
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

    def get_introduction(self):
        result = "**{} ({:%d-%b-%Y})**\r\n\r\n".format(
            self._name,
            date.today())
        result += "_{}_:\r\n\r\n".format(self._introduction)
        return result

    def get_report(self):
        return None, 0, None


class SqlReport(Report):
    def __init__(self, sql, conn=None, parameters=None, **kwargs):

        super().__init__(**kwargs)
        self._sql = sql
        self._conn = conn or DatabaseConnection.reporting
        self._parameters = parameters or ()

    def get_report(self):
        attachments = None

        with self._conn() as conn:

            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(self._sql, self._parameters)

                if cursor.rowcount == 0:
                    return None, 0, attachments

                report, rows = self.get_report_lines(cursor)

        markdown = self.get_introduction()
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


class PdfReport(SqlReport):
    def __init__(self, template, **kwargs):

        super().__init__(**kwargs)
        self._template = template

    def get_report(self):

        env = Environment(loader=FileSystemLoader('./templates'))

        template = env.get_template(self._template)

        with self._conn() as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute(self._sql, self._parameters)

                template_vars = {
                    "rows": cursor.fetchall(),
                    "now": datetime.datetime.utcnow()
                }

                html = template.render(template_vars)

                buf = io.BytesIO()
                HTML(string=html, base_url='.').write_pdf(buf)
                buf.seek(0)

        mkdn = self.get_introduction()

        attachments = [{
            'filename': '{}.pdf'.format(self._name),
            'inline': False,
            'stream': buf
        }]

        return mkdn, 1, attachments


def get_concrete_reports(cls=None):

    if (cls is None):
        cls = Report

    result = [sub() for sub in cls.__subclasses__()
              if len(sub.__subclasses__()) == 0]

    for sub in [sub for sub in cls.__subclasses__()
                if len(sub.__subclasses__()) != 0]:
        result += get_concrete_reports(sub)

    return result
