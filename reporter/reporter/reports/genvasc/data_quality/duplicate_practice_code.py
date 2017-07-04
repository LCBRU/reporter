#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_GENVASC_ADMIN


class GenvascDuplicatePracticeCode(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following practice codes "
                          "are duplicated in the GENVASC rollout "
                          "REDCap data"),
            recipients=[RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.never,
            sql='''

SELECT practice_code
FROM    (
    SELECT LEFT(value, CHARINDEX('(', value + '(') - 1) [practice_code]
    FROM STG_redcap.dbo.redcap_data
    WHERE   field_name = 'practice_code'
        AND project_id = 41
    UNION ALL
    SELECT LEFT(value, CHARINDEX('(', value + '(') - 1) [practice_code]
    FROM STG_redcap_briccsext.dbo.redcap_data
    WHERE   field_name = 'practice_code'
        AND project_id = 29
) x
GROUP BY practice_code
HAVING COUNT(*) > 1

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['practice_code'])
