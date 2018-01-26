#!/usr/bin/env python3

from reporter.reports import SqlReport, Schedule
from reporter.reports.emailing import RECIPIENT_GENVASC_ADMIN


class GenvascDuplicatePracticeCode(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following practice codes "
                          "are duplicated in the GENVASC rollout "
                          "REDCap data"),
            recipients=[RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.daily,
            sql='''

SELECT practice_code
FROM    (
    SELECT DISTINCT
        record,
        LEFT(value, CHARINDEX('(', value + '(') - 1) [practice_code]
    FROM STG_redcap_briccsext.dbo.redcap_data
    WHERE   field_name = 'practice_code'
        AND project_id IN (
            29,
            53
        )
) x
GROUP BY practice_code
HAVING COUNT(*) > 1

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['practice_code'])
