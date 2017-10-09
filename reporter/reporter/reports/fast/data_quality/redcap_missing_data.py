#!/usr/bin/env python3

from reporter.reports import Report
from reporter import (
    RedcapInstance,
    RECIPIENT_FAST_ADMIN
)

# Abstract Reports


class FastRedcapMissingData(Report):
    def __init__(self):
        self._redcap_instance = RedcapInstance.internal
        project_id = 43
        fields = ['nhs_number', 'gender', 'ethnicity', 'dob',
                  'date', 'practice_location', 'invitation_grp',
                  'invitation_type', 'iti_max_ap', 'iti_max_trnsvrs',
                  'sys_bp', 'dias_bp', 'pulse']
        recipients = [RECIPIENT_FAST_ADMIN]
        schedule = None

        super().__init__(
            introduction=("The following participants have data "
                          "missing from REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    {1}.dbo.redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN STG_redcap.dbo.redcap_metadata md
        ON md.project_id = r.project_id
        AND md.field_name IN ({0})
)
SELECT
    pe.project_id,
    pe.record,
    pe.error AS [error_message]
FROM potential_errors pe
WHERE NOT EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
AND EXISTS (
    SELECT 1
    FROM    [i2b2_app03_fast_Data].[dbo].[LOAD_FullyConsented] fc
    WHERE fc.StudyNumber = pe.record

)
ORDER BY pe.record

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields]),
                self._redcap_instance()['staging_database']),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )
