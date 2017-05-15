#!/usr/bin/env python3

import pymssql
import smtplib
import markdown
import requests
import os
import datetime
import logging
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import matplotlib
matplotlib.use('Agg')


SQL_HOST = os.environ["SQL_HOST"]
SQL_USER = os.environ["SQL_USER"]
SQL_PASSWORD = os.environ["SQL_PASSWORD"]
SQL_DATABASE = os.environ["SQL_DATABASE"]

EMAIL_FROM_ADDRESS = os.environ["EMAIL_FROM_ADDRESS"]
EMAIL_SMTP_SERVER = os.environ["EMAIL_SMTP_SERVER"]

SLACK_DATA_CHANNEL_URL = os.environ["SLACK_DATA_CHANNEL_URL"]
DEFAULT_RECIPIENT = os.environ["DEFAULT_RECIPIENT"]


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_report_db():
    return pymssql.connect(SQL_HOST, SQL_USER, SQL_PASSWORD, SQL_DATABASE)


def send_markdown_email(
    report_name,
    recipient,
    mkdn,
    attachments=[]
):

    msg = MIMEMultipart()
    msg['Subject'] = report_name
    msg['To'] = recipient
    msg['From'] = EMAIL_FROM_ADDRESS

    html = markdown.markdown(mkdn)
    msg.attach(MIMEText(html, 'html'))

    for a in attachments:
        part = MIMEImage(a['stream'].read())

        part.add_header('Content-Disposition',
                        'inline; filename="{}"'.format(a['filename']))
        part.add_header('Content-ID', a['filename'])
        msg.attach(part)

    s = smtplib.SMTP(EMAIL_SMTP_SERVER)
    s.send_message(msg)
    s.quit()

    logging.info(f"{report_name} Email Sent")


def send_markdown_slack(report_name, mkdn):
    # Convert to Slack markdown
    mkdn = mkdn.replace('**', '*')  # Headings
    mkdn = re.sub('\[(.*)]\((.*)\)', '<\g<2>|\g<1>>', mkdn)  # Links

    r = requests.post(
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

    logging.info(f"{report_name} Slack Sent")


def get_recipient(recipient):
    return os.getenv(recipient, DEFAULT_RECIPIENT)


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
