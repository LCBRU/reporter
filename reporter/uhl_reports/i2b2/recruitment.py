#!/usr/bin/env python3

import io
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from reporter.core import SqlReport


class CumulativeRecruitment(SqlReport):
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
    WHERE ConsentDate IS NOT NULL
) x
GROUP BY ConsentDate
ORDER BY ConsentDate

            '''.format(database)
        )

    def get_report(self):

        with self._conn() as cursor:

            df = pd.io.sql.read_sql(
                self._sql,
                cursor.connection,
                index_col='ConsentDate')

            fig, ax = plt.subplots()

            ax.set_title(self._name)

            ax.plot(df, label='Frequency')

            df = df.cumsum()

            ax.plot(df, label='Cumulative')

            if df.empty:
                datemin = datetime.date(datetime.datetime.now().year, 1, 1)
                datemax = datemin
                total_recruited = 0
            else:
                datemin = datetime.date(int(df.index.year.min()), 1, 1)
                datemax = datetime.date(int(df.index.year.max()) + 1, 1, 1)
                total_recruited = df.ct[-1]

            ax.set_xlim(datemin, datemax)
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            ax.set_ylabel('No. of Recruits')
            ax.set_xlabel('Consent Date')
            ax.legend()
            fig.autofmt_xdate()

            ax.annotate(
                'Total Recruitment*: {}'.format(total_recruited),
                xy=(df.index.max(), total_recruited),
                bbox=dict(boxstyle="square, pad=0.6", alpha=0.2),
                xytext=(0.1, 0.7),
                textcoords='axes fraction',
            )

            fig.text(
                0.01,
                0.01,
                '* including recruited statuses only',
                fontsize=10
            )

            ax.grid(True, linestyle='dotted')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            mkdn = "![{}](cid:recruitment.png)\r\n\r\n".format(
                self._name)

            attachments = [{
                'filename': 'recruitment.png',
                'inline': True,
                'stream': buf
            }]

            return mkdn, 1, attachments
