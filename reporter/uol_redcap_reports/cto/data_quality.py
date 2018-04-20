#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRAVE_MANAGER as RECIPIENT_MANAGER,
)

REDCAP_PROJECT_ID = 15

# Abstract Reports


class RedcapInvalidNhsNumber(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid NHS Number "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class CtoRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_PROJECT_ID,
            fields=['nhs_num'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


