#!/usr/bin/env python3

import pymssql
import smtplib
import markdown
import requests
import os
import datetime
import logging
import re
from email.mime.text import MIMEText


SQL_HOST = os.environ["SQL_HOST"]
SQL_USER = os.environ["SQL_USER"]
SQL_PASSWORD = os.environ["SQL_PASSWORD"]
SQL_DATABASE = os.environ["SQL_DATABASE"]

EMAIL_FROM_ADDRESS = os.environ["EMAIL_FROM_ADDRESS"]
EMAIL_SMTP_SERVER = os.environ["EMAIL_SMTP_SERVER"]

SLACK_DATA_CHANNEL_URL = os.environ["SLACK_DATA_CHANNEL_URL"]


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def get_report_db():
    return pymssql.connect(SQL_HOST, SQL_USER, SQL_PASSWORD, SQL_DATABASE)


def send_markdown_email(report_name, recipient, mkdn):
    html = markdown.markdown(mkdn)
    msg = MIMEText(html, 'html')

    msg['Subject'] = report_name
    msg['To'] = recipient
    msg['From'] = EMAIL_FROM_ADDRESS

    s = smtplib.SMTP(EMAIL_SMTP_SERVER)
    s.send_message(msg)
    s.quit()

    logging.info(f"{report_name} Email Sent")


def send_markdown_slack(report_name, mkdn):
    # Convert to Slack markdown
    mkdn = mkdn.replace('**', '*') # Headings
    mkdn = re.sub('\[(.*)]\((.*)\)', '<\g<2>|\g<1>>', mkdn) # Links

    r = requests.post(
    	SLACK_DATA_CHANNEL_URL,
    	json = {
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
