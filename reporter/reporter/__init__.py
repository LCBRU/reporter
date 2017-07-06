#!/usr/bin/env python3

import pymssql
import smtplib
import markdown
import requests
import os
import logging
import re
from enum import Enum
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
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

SLACK_DATA_CHANNEL_URL = os.environ["SLACK_DATA_CHANNEL_URL"]
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
RECIPIENT_TMAO_MANAGER = 'RECIPIENT_SCAD_MANAGER'
RECIPIENT_TMAO_ADMIN = 'RECIPIENT_SCAD_ADMIN'


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
        part = MIMEImage(a['stream'].read())

        part.add_header('Content-Disposition',
                        'inline; filename="{}"'.format(a['filename']))
        part.add_header('Content-ID', a['filename'])
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


def send_markdown_slack(report_name, mkdn):
    # Convert to Slack markdown
    mkdn = mkdn.replace('**', '*')  # Headings
    mkdn = re.sub('\[(.*)]\((.*)\)', '<\g<2>|\g<1>>', mkdn)  # Links

    requests.post(
        SLACK_DATA_CHANNEL_URL,
        json={
            'text': report_name,
            'mrkdwn': True,
            'attachments': [{
                'text': mkdn,
                'mrkdwn_in': ['text']
            }]
        },
        headers={'Content-Type': 'application/json'}
    )

    logging.info("{} Slack Sent".format(report_name))


def get_case_link(link_text, case_id, contact_id):
    CIVICRM_CASE_URL = ('[{}]('
                        'http://lcbru.xuhl-tr.nhs.uk/civicrm/contact/view/case'
                        '?id={}&cid={})')

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
