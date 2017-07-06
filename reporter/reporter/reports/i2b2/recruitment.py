#!/usr/bin/env python3

import io
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from reporter.reports import Report, Schedule
from reporter import (
    RECIPIENT_BIORESOURCE_MANAGER,
    RECIPIENT_BRICCS_MANAGER,
    RECIPIENT_IT_DQ,
    RECIPIENT_LAB_MANAGER
)


class CumulativeRecruitment(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    ConsentDate,
    COUNT(*) AS ct
FROM (
    SELECT
          DATEADD(
            month,
            DATEDIFF(month, 0, [ConsentDate]),
            0) AS ConsentDate
    FROM {}.[dbo].[PatientSummary]
) x
GROUP BY ConsentDate
ORDER BY ConsentDate

            '''.format(database),
            send_slack=False)

    def get_report(self):

        with self._conn() as conn:

            df = pd.io.sql.read_sql(
                self._sql,
                conn,
                index_col='ConsentDate')

            fig, ax = plt.subplots()

            ax.set_title(self._name)

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
                'Total Recruitment*: {}'.format(df.ct[-1]),
                xy=(df.index.max(), df.ct[-1]),
                bbox=dict(boxstyle="square, pad=0.6", alpha=0.2),
                xytext=(0.1, 0.7),
                textcoords='axes fraction',
            )

            fig.text(
                0.01,
                0.01,
                '* including \'recruited\' status only',
                fontsize=10
            )

            ax.grid(True, linestyle='dotted')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            mkdn = "![{}](cid:recruitment.png)\r\n\r\n".format(
                self._name)

            attachments = [{'filename': 'recruitment.png', 'stream': buf}]

            return mkdn, 1, attachments


class BioresourceCumulativeRecruitment(
        CumulativeRecruitment):
    def __init__(self):
        super().__init__(
            'i2b2_app03_bioresource_Data',
            [
                RECIPIENT_BIORESOURCE_MANAGER,
                RECIPIENT_IT_DQ,
                RECIPIENT_LAB_MANAGER])


class BriccsCumulativeRecruitment(
        CumulativeRecruitment):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            [
                RECIPIENT_BRICCS_MANAGER,
                RECIPIENT_IT_DQ,
                RECIPIENT_LAB_MANAGER],
            schedule=Schedule.never)
