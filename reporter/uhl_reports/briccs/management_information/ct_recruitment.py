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
	SUM(CASE WHEN [CT requested by UHL team] = 1 AND ps.withPlasma = 1 THEN 1 ELSE 0 END) [CT requested by UHL team],
	SUM(CASE WHEN [CT received by UHL team] = 1 AND ps.withPlasma = 1 THEN 1 ELSE 0 END) [CT received by UHL team],
	SUM(completeWithplasma) [completeWithplasma],
	CASE
		WHEN ps.RecruitingSite = 'briccs_glenfield_recruitment' THEN SUM(ps.withPlasma)
		ELSE SUM(CASE WHEN [CT received by UHL team] = 1 AND ps.withPlasma = 1 THEN 1 ELSE 0 END)
	END - SUM(completeWithplasma) [CT Awaiting Analysis]
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
	'Glenfield' Site,
	StudyNumber,
	lrc.project_id,
	'local' as redcap,
	lrc.consent_date
FROM [i2b2_app03_b1_data].[dbo].[LOAD_Redcap] lrc
JOIN STG_redcap.dbo.redcap_data studycode
	ON studycode.project_id = lrc.project_id
	AND studycode.record = lrc.StudyNumber
	AND studycode.field_name = 'epi_studycode'
	AND studycode.value = 8
WHERE lrc.Full_Consent = 1
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
	AND NOT EXISTS (
		SELECT 1
		FROM STG_redcap.dbo.redcap_data ct_analysed
		WHERE ct_analysed.project_id = lrc.project_id
			AND ct_analysed.record = lrc.StudyNumber
			AND ct_analysed.field_name = 'ct_date_time_start'
			AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_analysed.value) = 0
	) AND NOT EXISTS (
		SELECT 1
		FROM STG_redcap.dbo.redcap_data blood_not_taken
		WHERE blood_not_taken.project_id = lrc.project_id
			AND blood_not_taken.record = lrc.StudyNumber
			AND blood_not_taken.field_name = 'blood_taken'
			AND COALESCE(blood_not_taken.value, 0) = 0
	)

UNION

SELECT
	REPLACE(REPLACE(lrc.project_name, 'briccs_', ''), '_recruitment', '') Site,
	StudyNumber,
	lrc.project_id,
	'external' as redcap,
	lrc.consent_date
FROM [i2b2_app03_b1_data].[dbo].[LOAD_RedcapExternal] lrc
JOIN STG_redcap_briccsext.dbo.redcap_data studycode
	ON studycode.project_id = lrc.project_id
	AND studycode.record = lrc.StudyNumber
	AND studycode.field_name = 'epi_studycode'
	AND studycode.value = 8
JOIN STG_redcap_briccsext.dbo.redcap_data ct_requested
	ON ct_requested.project_id = lrc.project_id
	AND ct_requested.record = lrc.StudyNumber
	AND ct_requested.field_name = 'date_ct_reqd_iep'
	AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_requested.value) = 0
	-- Only interested in recruited that have been analysed
JOIN STG_redcap_briccsext.dbo.redcap_data ct_received
	ON ct_received.project_id = lrc.project_id
	AND ct_received.record = lrc.StudyNumber
	AND ct_received.field_name = 'iep_receipt_yn'
	AND ct_received.record = ct_requested.record
	AND COALESCE(ct_received.value, 0) = 1
WHERE lrc.Full_Consent = 1
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
	AND NOT EXISTS (
		SELECT 1
		FROM STG_redcap_briccsext.dbo.redcap_data ct_analysed
		WHERE ct_analysed.project_id = lrc.project_id
			AND ct_analysed.record = lrc.StudyNumber
			AND ct_analysed.field_name = 'ct_date_time_start'
			AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_analysed.value) = 0
	) AND NOT EXISTS (
		SELECT 1
		FROM STG_redcap_briccsext.dbo.redcap_data blood_not_taken
		WHERE blood_not_taken.project_id = lrc.project_id
			AND blood_not_taken.record = lrc.StudyNumber
			AND blood_not_taken.field_name = 'blood_taken'
			AND COALESCE(blood_not_taken.value, 0) = 0
	)
ORDER BY consent_date ASC

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
            datetime.datetime.strptime(row['consent_date'], '%Y-%m-%d'),
        )
