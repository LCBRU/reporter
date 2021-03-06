#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)
from reporter.connections import get_redcap_link


class FastEq5dNotSent(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants' baseline "
                          "is over 6 months old, but their EQ-5D 6 month "
                          "follow up questionnaire has not been sent :"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.never,
            sql='''

WITH due AS (
    SELECT
        project_id,
        record,
        DATEDIFF(d, CONVERT(DATE, value), GETDATE()) [age],
        CONVERT(DATETIME, value) baseline_date
    FROM    STG_redcap.dbo.redcap_data
    WHERE   project_id = 43
        AND field_name = 'date_qol_baseline'
        AND DATEDIFF(d, CONVERT(DATE, value), GETDATE()) > 180
)
SELECT d.*
FROM due d
LEFT JOIN STG_redcap.dbo.redcap_data sent
    ON sent.project_id = d.project_id
    AND sent.record = d.record
    AND sent.field_name = 'eq5d_6mth_sent_yn'
WHERE COALESCE(sent.value, '0') = '0'
	AND NOT EXISTS (
		SELECT 1
		FROM STG_redcap.dbo.redcap_data w
		WHERE w.project_id = d.project_id
			AND w.record = d.record
			AND ((	w.field_name IN ('non_complete_rsn', 'wthdrwl_date')
					AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(w.value) = 0
				) OR (
					w.field_name = 'study_status_comp_yn'
						AND COALESCE(value, 1) = 0
				))
	)
;

                '''
        )

    def get_report_line(self, row):
        return '- {}: Baseline = {:%d %B %Y} ({} days ago)\r\n'.format(
            get_redcap_link(
                row['record'], row['project_id'], row['record']),
            row['baseline_date'],
            row['age']
        )
