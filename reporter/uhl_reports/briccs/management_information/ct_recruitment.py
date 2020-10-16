#!/usr/bin/env python3

import pandas as pd
import datetime
from reporter.core import SqlReport, Schedule
from reporter.emailing import RECIPIENT_BRICCSCT_ANALYSERS, RECIPIENT_BRICCSCT_MI
from reporter.connections import RedcapInstance


class BriccsCtRecruitment(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("BRICCS CT Recruitment"),
            recipients=[RECIPIENT_BRICCSCT_ANALYSERS, RECIPIENT_BRICCSCT_MI],
			sql='''

SELECT
    REPLACE(REPLACE(ps.RecruitingSite, 'Briccs_', ''), '_Recruitment', '') Site,
    COUNT(*) TotalRecruitment,
    MIN(we.withdrawn) Withdrawn,
    MIN(we.excluded) Excluded,
    SUM(ps.withPlasma) WithPlasma,
    SUM([CT requested by UHL team with plasma]) [CT requested by UHL team],
    SUM([CT received by UHL team with plasma]) [CT received by UHL team],
    SUM(completeWithplasma) [completeWithplasma],
    SUM([CT Awaiting Analysis]) [CT Awaiting Analysis]
FROM [i2b2_app03_b1_data].dbo.Cache_PatientSummary ps
LEFT JOIN (
    SELECT
        'briccs_glenfield_recruitment' RecruitingSite,
        SUM(lrc.is_withdrawn) [withdrawn],
        SUM(lrc.is_excluded) [excluded]
    FROM [i2b2_app03_b1_data].[dbo].[LOAD_Redcap] lrc
    JOIN STG_redcap.dbo.redcap_data studycode
        ON studycode.project_id = lrc.project_id
        AND studycode.record = lrc.StudyNumber
        AND studycode.field_name = 'epi_studycode'
        AND studycode.value = 8

    UNION

    SELECT
        'briccs_kettering_recruitment' RecruitingSite,
        SUM(lrc.is_withdrawn) [withdrawn],
        SUM(lrc.is_excluded) [excluded]
    FROM [i2b2_app03_b1_data].[dbo].[LOAD_RedcapExternal] lrc
    JOIN STG_redcap_briccsext.dbo.redcap_data studycode
        ON studycode.project_id = lrc.project_id
        AND studycode.record = lrc.StudyNumber
        AND studycode.field_name = 'epi_studycode'
        AND studycode.value = 8
    ) we ON we.RecruitingSite = ps.RecruitingSite
WHERE
    In_BRICCS_CT_Study = 1
GROUP BY ps.RecruitingSite

			'''

        )

    def get_report(self):
        markdown = ''

        markdown += '# BRICCS CT Recruitment {0:%d-%b-%Y}\r\n\r\n'.format(datetime.datetime.now())
        markdown += 'Breakdown of CT recruitment and CT analysis figures.\r\n\r\n'

        columns = [
            'Site',
            'Total Recruited',
            'Withdrawn',
            'Excluded',
            'With Plasma',
            'CT Requested',
            'CT Received',
            'CT Analysed',
            'CT Awaiting Analysis',
        ]

        markdown += ' | '.join(columns) + '\r\n'
        markdown += ' | '.join(['-' * len(x) for x in columns]) + '\r\n'

        with self._conn() as cursor:

            df = pd.io.sql.read_sql(
                self._sql,
                cursor.connection,
                index_col='Site')

            df.loc['Total'] = df.sum(numeric_only=True)

            for index, row in df.iterrows():
                markdown += ' | '.join([str(v) for v in [
                    index.title(),
                    row['TotalRecruitment'],
                    row['Withdrawn'],
                    row['Excluded'],
                    row['WithPlasma'],
                    row['CT requested by UHL team'],
                    row['CT received by UHL team'],
                    row['completeWithplasma'],
                    row['CT Awaiting Analysis'], 
                ]]) + '\r\n'

            return markdown, 1, []


class BriccsCtOutstandingAnalysis(SqlReport):
    def __init__(self):

        super().__init__(
            introduction=("The following recruits have CT scans available that have not been analysed"),
            schedule=Schedule.daily,
            recipients=[RECIPIENT_BRICCSCT_ANALYSERS],
            sql='''

SELECT
    REPLACE(REPLACE(ps.RecruitingSite, 'Briccs_', ''), '_Recruitment', '') Site,
    ps.StudyNumber,
    ps.ConsentDate AS consent_date,
    we.redcap,
    we.project_id
FROM [i2b2_app03_b1_data].[dbo].[Cache_PatientSummary] ps
JOIN (

    SELECT lrc.StudyNumber,
        'local' AS redcap,
        lrc.project_id
    FROM [i2b2_app03_b1_data].[dbo].[LOAD_Redcap] lrc
    JOIN STG_redcap.dbo.redcap_data ct_date_time_start
        ON ct_date_time_start.project_id = lrc.project_id
        AND ct_date_time_start.record = lrc.StudyNumber
        AND ct_date_time_start.field_name = 'ct_date_time_start'
        AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_date_time_start.value) = 0

 UNION

    SELECT lrc.StudyNumber,
        'external' AS redcap,
        lrc.project_id
    FROM [i2b2_app03_b1_data].[dbo].[LOAD_RedcapExternal] lrc
    JOIN STG_redcap_briccsext.dbo.redcap_data imaging_completed
        ON imaging_completed.project_id = lrc.project_id
        AND imaging_completed.record = lrc.StudyNumber
        AND imaging_completed.field_name = 'cardiac_imaging_data_complete'
        AND imaging_completed.value = 1
    ) we ON we.StudyNumber = ps.StudyNumber
WHERE ps.In_BRICCS_CT_Study IS NOT NULL
 AND [CT Awaiting Analysis] = 1
 AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ps.UhlSystemNumber) = 0
ORDER BY ps.ConsentDate ASC

                '''
        )

    def get_report_line(self, row):
        redcap_instance = RedcapInstance.internal

        if row['redcap'] != 'local':
            redcap_instance = RedcapInstance.external

        return '- {0}: Recruited at {1} on {2:%d-%b-%Y}\r\n'.format(
            redcap_instance()['link_generator'](
                row['StudyNumber'],
                row['project_id'],
                row['StudyNumber']
            ),
            row['Site'].title(),
            row['consent_date'],
        )
