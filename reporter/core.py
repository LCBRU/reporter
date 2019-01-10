import schedule
import logging
import re
import datetime
import io
import time
import traceback
import importlib
import pkgutil
import inspect
from datetime import date
from enum import Enum
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from reporter.emailing import send_markdown_email
from reporter.connections import DatabaseConnection
from reporter.emailing import email_error


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
        try:
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
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            logging.error(traceback.format_exc())
            email_error(self._name, traceback.format_exc())

    def get_introduction(self):
        result = "**{} ({:%d-%b-%Y})**\r\n\r\n".format(
            self._name,
            date.today())
        result += "_{}_:\r\n\r\n".format(self._introduction)
        return result

    def get_report(self):
        return None, 0, None

    def get_details(self):
        return '"{}", "{}", "{}"'.format(
            self._name,
            self._schedule.__name__,
            "; ".join(self._recipients),
        )


class SqlReport(Report):
    def __init__(self, sql, conn=None, parameters=None, **kwargs):

        super().__init__(**kwargs)
        self._sql = sql
        self._conn = conn or DatabaseConnection.reporting
        self._parameters = parameters or ()

    def get_report(self):
        attachments = None

        with self._conn() as conn:

            conn.execute(self._sql, self._parameters)

            if conn.rowcount == 0:
                return None, 0, attachments

            report, rows = self.get_report_lines(conn)

        markdown = self.get_introduction()
        markdown += report
        markdown += "\r\n\r\n{} Record(s) Found".format(rows)

        return markdown, rows, attachments

    def get_report_lines(self, cursor):
        markdown = ''
        rows = 0

        for row in cursor:
            line = self.get_report_line(row)
            if line:
                rows += 1
                markdown += line

        return markdown, rows

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
            conn.execute(self._sql, self._parameters)

            template_vars = {
                "rows": conn.fetchall(),
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
              if len(sub.__subclasses__()) == 0 and
              # If the constructor requires parameters
              # other than self (i.e., it has more than 1
              # argument), it's an abstract class
              len(inspect.getfullargspec(sub.__init__)[0]) == 1]

    for sub in [sub for sub in cls.__subclasses__()
                if len(sub.__subclasses__()) != 0]:
        result += get_concrete_reports(sub)

    return result


def schedule_reports():
    reports = get_concrete_reports()

    for r in reports:
        r.schedule()

    logging.info("---- {} reports scheduled ----".format(len(reports)))

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info('Schedule stopped')
            return


def run_reports(report_name, exclude):
    reports = get_concrete_reports()

    for r in reports:

        if type(r).__name__.lower() in exclude:
            continue

        if type(r).__name__[:len(report_name)].lower() == report_name.lower():
            try:
                r.run()
            except KeyboardInterrupt:
                logging.info('Schedule stopped')
                return


def run_all(exclude):
    reports = get_concrete_reports()

    for r in reports:

        if type(r).__name__.lower() in exclude:
            continue

        r.run()


def list_all():
    for r in get_concrete_reports():
        print(r.get_details())


def get_sub_modules(path, prefix):
    result = []

    for m in pkgutil.iter_modules(path):
        new_module_name = prefix + m[1]
        result.append(new_module_name)
        result.extend(get_sub_modules(
            [path[0] + '/' + m[1]],
            new_module_name + '.'
        ))

    return result


def import_sub_reports(path, name):
    for m in get_sub_modules(path, name + '.'):
        importlib.import_module(m)
