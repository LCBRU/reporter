#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)
from reporter.reports.redcap import get_redcap_link


class FastEq5dNotEntered(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants have "
                          "returned the EQ-5D follow up questionnaire, "
                          "but it has not been entered:"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''

WITH received AS (
    SELECT
        project_id,
        record
    FROM    STG_redcap.dbo.redcap_data
    WHERE   project_id = 43
        AND field_name = 'date_6mnth_eq5d_recd'
        AND value = '1'
)
SELECT r.*
FROM received r
WHERE NOT EXISTS (
    SELECT 1
    FROM    STG_redcap.dbo.redcap_data v
    WHERE v.project_id = r.project_id
        AND v.record = r.project_id
        AND v.field_name IN (
            'mobility_6_mnth',
            'self_care_6_mnth',
            'usual_activities_6_mnth',
            'pain_discomfort_6_mnth',
            'anxiety_6_mnth',
            'scale_health_6_mnth')
        AND LEN(LTRIM(RTRIM(COALESCE(v.value, '')))) > 0
)
;

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_redcap_link(
                row['record'], row['project_id'], row['record'])
        )
