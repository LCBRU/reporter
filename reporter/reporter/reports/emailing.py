#!/usr/bin/env python3

import smtplib
import markdown
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from email.mime.text import MIMEText


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
RECIPIENT_CARDIOMET_MANAGER = 'RECIPIENT_CARDIOMET_MANAGER'
RECIPIENT_CARDIOMET_ADMIN = 'RECIPIENT_CARDIOMET_ADMIN'
RECIPIENT_GENVASC_MANAGER = 'RECIPIENT_GENVASC_MANAGER'
RECIPIENT_GENVASC_ADMIN = 'RECIPIENT_GENVASC_ADMIN'
RECIPIENT_GRAPHIC2_MANAGER = 'RECIPIENT_GRAPHIC2_MANAGER'
RECIPIENT_GRAPHIC2_ADMIN = 'RECIPIENT_GRAPHIC2_ADMIN'
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
RECIPIENT_MINERVA_MANAGER = 'RECIPIENT_MINERVA_MANAGER'
RECIPIENT_MINERVA_ADMIN = 'RECIPIENT_MINERVA_ADMIN'
RECIPIENT_PREDICT_MANAGER = 'RECIPIENT_PREDICT_MANAGER'
RECIPIENT_PREDICT_ADMIN = 'RECIPIENT_PREDICT_ADMIN'
RECIPIENT_SPIRAL_MANAGER = 'RECIPIENT_SPIRAL_MANAGER'
RECIPIENT_SPIRAL_ADMIN = 'RECIPIENT_SPIRAL_ADMIN'


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


def email_error(report_name, error_text):
    msg = MIMEText(error_text)
    msg['Subject'] = 'Reporter: Error in ' + report_name
    msg['To'] = DEFAULT_RECIPIENT
    msg['From'] = EMAIL_FROM_ADDRESS

    s = smtplib.SMTP(EMAIL_SMTP_SERVER)
    s.send_message(msg)
    s.quit()


def get_recipients(recipients):
    result = set()

    recipients.append(RECIPIENT_IT_DQ)

    list_of_recs = [os.getenv(r) for r in recipients]

    for lr in list_of_recs:
        if lr:
            result |= set(lr.split(','))

    if len(result) == 0:
        result = set([DEFAULT_RECIPIENT])

    return result
