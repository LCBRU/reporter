#!/usr/bin/env python3

import pandas as pd
import datetime
from reporter.core import SqlReport, Schedule
from reporter.emailing import RECIPIENT_BRICCSCT_ANALYSERS, RECIPIENT_BRICCSCT_MI
from reporter.connections import RedcapInstance


class BriccsCtRecruitment(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following Glenfield participants are "
                          "in Onyx, but are not in CiviCrm"),
            recipients=[RECIPIENT_BRICCSCT_ANALYSERS, RECIPIENT_BRICCSCT_MI],
            sql='''

SELECT
	'Glenfield' Site,
	COUNT(StudyNumber)[total_recruited],
	SUM(lrc.is_withdrawn) [withdrawn],
	SUM(lrc.is_excluded) [excluded],
	COUNT(blood_not_taken.record) [blood_not_taken],
	COUNT(StudyNumber) - SUM(lrc.is_withdrawn) - SUM(lrc.is_excluded) - COUNT(blood_not_taken.record) [for_analysis],
	0  [ct_requested],
	COUNT(StudyNumber) - SUM(lrc.is_withdrawn) - SUM(lrc.is_excluded) - COUNT(blood_not_taken.record) [ct_received_or_at_glenfield],
	COUNT(ct_analysed.record) [analysed],
	COUNT(StudyNumber) - COUNT(ct_analysed.record) - SUM(lrc.is_withdrawn) - SUM(lrc.is_excluded)  - COUNT(blood_not_taken.record) [to_be_analysed]
FROM [i2b2_app03_b1_data].[dbo].[LOAD_Redcap] lrc
JOIN STG_redcap.dbo.redcap_data studycode
	ON studycode.project_id = lrc.project_id
	AND studycode.record = lrc.StudyNumber
	AND studycode.field_name = 'epi_studycode'
	AND studycode.value = 8
LEFT JOIN STG_redcap.dbo.redcap_data blood_not_taken
	ON blood_not_taken.project_id = lrc.project_id
	AND blood_not_taken.record = lrc.StudyNumber
	AND blood_not_taken.field_name = 'blood_taken'
	AND COALESCE(blood_not_taken.value, 0) = 0
	-- Only interested in recruited that have not had blood taken
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
LEFT JOIN STG_redcap.dbo.redcap_data ct_analysed
	ON ct_analysed.project_id = lrc.project_id
	AND ct_analysed.record = lrc.StudyNumber
	AND blood_not_taken.record IS NULL
	AND ct_analysed.field_name = 'ct_date_time_start'
	AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_analysed.value) = 0
	-- Only interested in recruited that have been analysed
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
WHERE lrc.Full_Consent = 1

UNION

SELECT
	REPLACE(REPLACE(lrc.project_name, 'briccs_', ''), '_recruitment', '') Site,
	COUNT(StudyNumber)[total_recruited],
	SUM(lrc.is_withdrawn) [withdrawn],
	SUM(lrc.is_excluded) [excluded],
	COUNT(blood_not_taken.record) [blood_not_taken],
	COUNT(StudyNumber) - SUM(lrc.is_withdrawn) - SUM(lrc.is_excluded) - COUNT(blood_not_taken.record) [for_analysis],
	COUNT(ct_requested.record) [ct_requested],
	COUNT(ct_received.record)  [ct_received_or_at_glenfield],
	COUNT(ct_analysed.record) [analysed],
	COUNT(ct_received.record) - COUNT(ct_analysed.record) [to_be_analysed]
FROM [i2b2_app03_b1_data].[dbo].[LOAD_RedcapExternal] lrc
JOIN STG_redcap_briccsext.dbo.redcap_data studycode
	ON studycode.project_id = lrc.project_id
	AND studycode.record = lrc.StudyNumber
	AND studycode.field_name = 'epi_studycode'
	AND studycode.value = 8
LEFT JOIN STG_redcap_briccsext.dbo.redcap_data blood_not_taken
	ON blood_not_taken.project_id = lrc.project_id
	AND blood_not_taken.record = lrc.StudyNumber
	AND blood_not_taken.field_name = 'blood_taken'
	AND COALESCE(blood_not_taken.value, 0) = 0
	-- Only interested in recruited that have not had blood taken
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
LEFT JOIN STG_redcap_briccsext.dbo.redcap_data ct_requested
	ON ct_requested.project_id = lrc.project_id
	AND ct_requested.record = lrc.StudyNumber
	AND blood_not_taken.record IS NULL
	AND ct_requested.field_name = 'date_ct_reqd_iep'
	AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_requested.value) = 0
	-- Only interested in recruited that have been analysed
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
LEFT JOIN STG_redcap_briccsext.dbo.redcap_data ct_received
	ON ct_received.project_id = lrc.project_id
	AND ct_received.record = lrc.StudyNumber
	AND ct_received.field_name = 'iep_receipt_yn'
	AND ct_received.record = ct_requested.record
	AND blood_not_taken.record IS NULL
	AND COALESCE(ct_received.value, 0) = 1
	-- Only interested in recruited that have been analysed
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
LEFT JOIN STG_redcap_briccsext.dbo.redcap_data ct_analysed
	ON ct_analysed.project_id = lrc.project_id
	AND ct_analysed.record = lrc.StudyNumber
	AND ct_analysed.record = ct_received.record
	AND blood_not_taken.record IS NULL
	AND ct_analysed.field_name = 'ct_date_time_start'
	AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(ct_analysed.value) = 0
	-- Only interested in recruited that have been analysed
	AND lrc.is_excluded = 0
	AND lrc.is_withdrawn = 0
WHERE lrc.Full_Consent = 1
GROUP BY lrc.project_name


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
            'Blood not Taken',
            'For CT Analysis',
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
                    row['total_recruited'],
                    row['withdrawn'],
                    row['excluded'],
                    row['blood_not_taken'],
                    row['for_analysis'],
                    row['ct_requested'],
                    row['ct_received_or_at_glenfield'],
                    row['analysed'],
                    row['to_be_analysed'], 
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
