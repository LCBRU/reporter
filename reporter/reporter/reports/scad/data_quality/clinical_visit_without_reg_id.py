#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.reports.redcap import get_redcap_link
from reporter.emailing import RECIPIENT_SCAD_ADMIN


class ClinicalVisitWithoutRegId(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following clinical visit records "
                          "do not have a SCAD Registration ID: "),
            recipients=[RECIPIENT_SCAD_ADMIN],
            sql='''

WITH participants AS (
    SELECT  DISTINCT record, project_id
    FROM    STG_redcap.dbo.redcap_data
    WHERE project_id = 28
)
SELECT p.record,
    p.project_id
FROM participants p
WHERE NOT EXISTS (
    SELECT 1
    FROM    STG_redcap.dbo.redcap_data reg
    WHERE reg.project_id = 28
        AND reg.record = p.record
        AND reg.field_name = 'scadreg_id'
        AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(reg.value) = 0
)

                '''
        )

    def get_report_line(self, row):
        return "- **{}**\r\n".format(get_redcap_link(
            row['record'], row['project_id'], row['record']))
