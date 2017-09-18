#!/usr/bin/env python3

import pymssql
import smtplib
import markdown
import os
import logging
from enum import Enum
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from email.mime.text import MIMEText
import matplotlib
matplotlib.use('Agg')


SQL_REPORTING_HOST = os.environ["SQL_REPORTING_HOST"]
SQL_REPORTING_USER = os.environ["SQL_REPORTING_USER"]
SQL_REPORTING_PASSWORD = os.environ["SQL_REPORTING_PASSWORD"]
SQL_REPORTING_DATABASE = os.environ["SQL_REPORTING_DATABASE"]

SQL_DWBRICCS_HOST = os.environ["SQL_DWBRICCS_HOST"]
SQL_DWBRICCS_USER = os.environ["SQL_DWBRICCS_USER"]
SQL_DWBRICCS_PASSWORD = os.environ["SQL_DWBRICCS_PASSWORD"]
SQL_DWBRICCS_DATABASE = os.environ["SQL_DWBRICCS_DATABASE"]

EMAIL_FROM_ADDRESS = os.environ["EMAIL_FROM_ADDRESS"]
EMAIL_SMTP_SERVER = os.environ["EMAIL_SMTP_SERVER"]

DEFAULT_RECIPIENT = os.environ["DEFAULT_RECIPIENT"]

RECIPIENT_IT_DWH = 'RECIPIENT_IT_DWH'
RECIPIENT_IT_DQ = 'RECIPIENT_IT_DQ'
RECIPIENT_LAB_MANAGER = 'RECIPIENT_LAB_MANAGER'
RECIPIENT_BIORESOURCE_MANAGER = 'RECIPIENT_BIORESOURCE_MANAGER'
RECIPIENT_BIORESOURCE_ADMIN = 'RECIPIENT_BIORESOURCE_ADMIN'
RECIPIENT_BRICCS_MANAGER = 'RECIPIENT_BRICCS_MANAGER'
RECIPIENT_BRICCS_ADMIN = 'RECIPIENT_BRICCS_ADMIN'
RECIPIENT_BRICCS_DQ = 'RECIPIENT_BRICCS_DQ'
RECIPIENT_GENVASC_MANAGER = 'RECIPIENT_GENVASC_MANAGER'
RECIPIENT_GENVASC_ADMIN = 'RECIPIENT_GENVASC_ADMIN'
RECIPIENT_GRAPHIC2_MANAGER = 'RECIPIENT_GRAPHIC2_MANAGER'
RECIPIENT_AS_MANAGER = 'RECIPIENT_AS_MANAGER'
RECIPIENT_AS_ADMIN = 'RECIPIENT_AS_ADMIN'
RECIPIENT_BRAVE_MANAGER = 'RECIPIENT_BRAVE_MANAGER'
RECIPIENT_BRAVE_ADMIN = 'RECIPIENT_BRAVE_ADMIN'
RECIPIENT_DREAM_MANAGER = 'RECIPIENT_DREAM_MANAGER'
RECIPIENT_DREAM_ADMIN = 'RECIPIENT_DREAM_ADMIN'
RECIPIENT_SCAD_MANAGER = 'RECIPIENT_SCAD_MANAGER'
RECIPIENT_SCAD_ADMIN = 'RECIPIENT_SCAD_ADMIN'
RECIPIENT_TMAO_MANAGER = 'RECIPIENT_TMAO_MANAGER'
RECIPIENT_TMAO_ADMIN = 'RECIPIENT_TMAO_ADMIN'
RECIPIENT_LENTEN_MANAGER = 'RECIPIENT_LENTEN_MANAGER'
RECIPIENT_LENTEN_ADMIN = 'RECIPIENT_LENTEN_ADMIN'
RECIPIENT_FAST_MANAGER = 'RECIPIENT_FAST_MANAGER'
RECIPIENT_FAST_ADMIN = 'RECIPIENT_FAST_ADMIN'
RECIPIENT_INDAPAMIDE_MANAGER = 'RECIPIENT_INDAPAMIDE_MANAGER'
RECIPIENT_INDAPAMIDE_ADMIN = 'RECIPIENT_INDAPAMIDE_ADMIN'
RECIPIENT_MARI_MANAGER = 'RECIPIENT_MARI_MANAGER'
RECIPIENT_MARI_ADMIN = 'RECIPIENT_MARI_ADMIN'


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class DatabaseConnection(Enum):
    def reporting():
        return pymssql.connect(
            SQL_REPORTING_HOST,
            SQL_REPORTING_USER,
            SQL_REPORTING_PASSWORD,
            SQL_REPORTING_DATABASE
        )

    def dwbriccs():
        return pymssql.connect(
            SQL_DWBRICCS_HOST,
            SQL_DWBRICCS_USER,
            SQL_DWBRICCS_PASSWORD,
            SQL_DWBRICCS_DATABASE
        )


def send_markdown_email(
    report_name,
    recipients,
    mkdn,
    attachments=None
):

    to_recipients = get_recipients(recipients)
    msg = MIMEMultipart()
    msg['Subject'] = report_name
    msg['To'] = ','.join(to_recipients)
    msg['From'] = EMAIL_FROM_ADDRESS

    html = markdown.markdown(mkdn)
    msg.attach(MIMEText(html, 'html'))

    for a in attachments or []:
        mimetype, encoding = guess_type(a['filename'])
        mimetype = mimetype.split('/', 1)
        part = MIMEBase(mimetype[0], mimetype[1])
        part.set_payload(a['stream'].read())
        encode_base64(part)

        if a['inline'] or False:
            part.add_header('Content-Disposition',
                            'inline; filename="{}"'.format(a['filename']))
            part.add_header('Content-ID', a['filename'])
        else:
            part.add_header('Content-Disposition',
                            'attachment; filename="{}"'.format(a['filename']))

        msg.attach(part)

    s = smtplib.SMTP(EMAIL_SMTP_SERVER)
    s.send_message(msg)
    s.quit()

    logging.info("{} Email Sent to {}".format(report_name, to_recipients))


def get_recipients(recipients):
    result = set()

    list_of_recs = [os.getenv(r) for r in recipients]

    for lr in list_of_recs:
        if lr:
            result |= set(lr.split(','))

    if len(result) == 0:
        result = set([DEFAULT_RECIPIENT])

    return result


def get_case_link(link_text, case_id, contact_id):
    CIVICRM_CASE_URL = ('[{}]('
                        'http://lcbru.xuhl-tr.nhs.uk/civicrm/contact/view/case'
                        '?id={}&cid={}&action=view)')

    return (CIVICRM_CASE_URL.format(
        link_text,
        case_id,
        contact_id))


def get_contact_link(link_text, contact_id):
    CIVICRM_CONTACT_URL = (
        '[{}]('
        'http://lcbru.xuhl-tr.nhs.uk/civicrm/contact/view'
        '?cid={})')

    return (CIVICRM_CONTACT_URL.format(
        link_text,
        contact_id))


def get_contact_id_search_link(link_text, contact_id):
    CIVICRM_SEARCH_URL = (
        '[{}]('
        'http://lcbru.xuhl-tr.nhs.uk/content/participant_search/{})')

    return (CIVICRM_SEARCH_URL.format(
        link_text,
        contact_id))


def get_redcap_link(link_text, project_id, record):
    REDCAP_VERSION = 'v7.2.2'
    REDCAP_RECORD_URL = (
        '[{}](https://briccs.xuhl-tr.nhs.uk/redcap/'
        'redcap_{}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_VERSION,
        project_id,
        record))


def get_redcap_external_link(link_text, project_id, record):
    REDCAP_VERSION = 'v7.2.2'
    REDCAP_RECORD_URL = (
        '[{}](https://uhlbriccsext01.xuhl-tr.nhs.uk/redcap/'
        'redcap_{}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_VERSION,
        project_id,
        record))
