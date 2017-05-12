#!/usr/bin/env python3

import schedule
import os
import io
import datetime
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from reporter import (get_report_db, send_markdown_email,
                      send_markdown_slack, get_recipient)


REPORT_NAME = 'Bioresource Cumulative Recruitment'


def bioresource_recruitment():

    markdown = ''

    with get_report_db() as conn:

        # query db
        sql = """

        SELECT ConsentDate, ct
        FROM CIVICRM_ScheduledReports_Bioresource_Recruitment
        ORDER BY ConsentDate

        """

        df = pd.io.sql.read_sql(sql, conn, index_col='ConsentDate')

        fig, ax = plt.subplots()

        ax.set_title(REPORT_NAME)

        ax.plot(df, label='Frequency')

        df = df.cumsum()

        ax.plot(df, label='Cumulative')

        datemin = datetime.date(df.index.year.min(), 1, 1)
        datemax = datetime.date(df.index.year.max() + 1, 1, 1)

        ax.set_xlim(datemin, datemax)
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.set_ylabel('No. of Recruits')
        ax.set_xlabel('Consent Date')
        ax.legend()
        fig.autofmt_xdate()

        ax.annotate(
            'Total Recruitment: {}'.format(df.ct[-1]),
            xy=(df.index.max(), df.ct[-1]),
            xytext=(0.1, 0.7),
            textcoords='axes fraction',
        )

        ax.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        mkdn = "![{}](cid:recruitment.png)\r\n\r\n".format(REPORT_NAME)

        attachments = [{'filename': 'recruitment.png', 'stream': buf}]

        send_markdown_email(
            REPORT_NAME,
            get_recipient("BIORESOURCE_RECRUITMENT_RECIPIENT"),
            mkdn,
            attachments
        )


# bioresource_recruitment()
schedule.every().monday.at("08:00").do(bioresource_recruitment)


logging.info(f"{REPORT_NAME} Loaded")
