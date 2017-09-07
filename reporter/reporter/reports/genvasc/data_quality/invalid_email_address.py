#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_GENVASC_ADMIN


class GenvascInvalidEmailAddress(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following email addresses are invalid "
                          "in the GENVASC practice details REDCap:"),
            recipients=[RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.daily,
            sql='''

SELECT DISTINCT
    p.app_title AS project_name,
    pc.value AS practice_code,
    md.element_label AS field_name,
    rd.value AS email_address
FROM    STG_redcap_briccsext.dbo.redcap_data rd
JOIN    STG_redcap_briccsext.dbo.redcap_metadata md
    ON md.project_id = rd.project_id
    AND md.field_name = rd.field_name
JOIN STG_redcap_briccsext.dbo.redcap_data pc
    ON pc.project_id = rd.project_id
    AND pc.field_name = 'practice_code'
    AND pc.record = rd.record
JOIN STG_redcap_briccsext.dbo.redcap_projects p
    ON p.project_id = rd.project_id
WHERE rd.project_id IN (29, 53)
    AND rd.field_name IN (
        'loc_lead_email',
        'local_contact_email',
        'practice_manager_email',
        'sen_part_email',
        'contact_email_add'
    )
    AND (
            i2b2ClinDataIntegration.dbo.isInvalidEmail(rd.value) = 1
        OR (
            rd.value NOT LIKE '%.nhs.uk'
            AND rd.value NOT LIKE '%@nhs.net'
        )
    )


                '''
        )

    def get_report_line(self, row):
        return '- {} - {}: {} = "{}"\r\n'.format(
            row['project_name'],
            row['practice_code'],
            row['field_name'],
            row['email_address'],
        )
