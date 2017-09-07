#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_GENVASC_ADMIN


class GenvascInvalidPracticeCode(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following practice codes are invalid "
                          "in the GENVASC practice details REDCap:"),
            recipients=[RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.daily,
            sql='''

SELECT
    p.app_title AS project_name,
    rd.value AS practice_code
FROM    STG_redcap_briccsext.dbo.redcap_data rd
JOIN    STG_redcap_briccsext.dbo.redcap_metadata md
    ON md.project_id = rd.project_id
    AND md.field_name = rd.field_name
JOIN STG_redcap_briccsext.dbo.redcap_projects p
    ON p.project_id = rd.project_id
WHERE rd.project_id IN (29, 53)
    AND rd.field_name IN (
        'practice_code'
    )
    AND i2b2ClinDataIntegration.dbo.isInvalidPracticeCode(rd.value) = 1

                '''
        )

    def get_report_line(self, row):
        return '- {} - {}\r\n'.format(
            row['project_name'],
            row['practice_code']
        )
