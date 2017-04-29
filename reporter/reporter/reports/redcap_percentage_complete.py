#!/usr/bin/env python3

import schedule
import os
import datetime
import logging
import math
from itertools import groupby
from reporter import get_report_db, send_markdown_email, send_markdown_slack

REPORT_NAME = 'REDCap Percentage Complete'
RECIPIENT = os.environ["REDCAP_PERCENTAGE_COMPLETE_RECIPIENT"]


def redcap_completeness(study_name):

    markdown = ""

    with get_report_db() as conn:

        with conn.cursor(as_dict=True) as cursor:
            cursor.execute('''
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
            ''', study_name)

            for project, forms in groupby(cursor, lambda r: (
                r['project_name'],
                r['last_used'])
            ):
                markdown += f"**{project[0]}**\r\n\r\n"
                markdown += f"_Last Used {project[1]::%d-%b-%Y}_:\r\n\r\n"

                for form in forms:
                    markdown += f"- **{form['form_name'].title()}**: "
                    markdown += f"{math.floor(form['perc'])}%\r\n\r\n"

            if cursor.rowcount > 0:
                send_markdown_email(
                    REPORT_NAME,
                    os.environ[
                        f"REDCAP_PERCENTAGE_COMPLETE_RECIPIENT_{study_name}"
                    ],
                    markdown
                )
                send_markdown_slack(REPORT_NAME, markdown)


schedule.every().monday.at("08:00").do(redcap_completeness, 'AS')
schedule.every().monday.at("08:00").do(redcap_completeness, 'Bioresource')
schedule.every().monday.at("08:00").do(redcap_completeness, 'BRAVE')
schedule.every().monday.at("08:00").do(redcap_completeness, 'BRICCS')
schedule.every().monday.at("08:00").do(redcap_completeness, 'DREAM')
schedule.every().monday.at("08:00").do(redcap_completeness, 'SCAD')
schedule.every().monday.at("08:00").do(redcap_completeness, 'TMAO')

logging.info(f"{REPORT_NAME} Loaded")
