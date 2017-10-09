#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN, get_redcap_link
)


class FastOutsideAgeRange(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants were recruited "
                          "outside the specified age range:"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.monthly,
            sql='''

SELECT
    dob.project_id,
    dob.record,
    [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, clinic_date.value)) AgeAtRecruitment
FROM    STG_redcap.dbo.redcap_data dob
JOIN    STG_redcap.dbo.redcap_data clinic_date
    ON clinic_date.project_id = dob.project_id
    AND clinic_date.record = dob.record
    AND clinic_date.field_name = 'date'
WHERE [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, clinic_date.value)) NOT BETWEEN 65 AND 74
    AND dob.project_id = 43
    AND dob.field_name = 'dob'

                '''
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            get_redcap_link(
                row['record'], row['project_id'], row['record']),
            row['AgeAtRecruitment']
        )
