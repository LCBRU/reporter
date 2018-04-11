#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.reports.emailing import RECIPIENT_SCAD_ADMIN
from reporter.reports.civicrm import get_contact_id_search_link


class DuplicateScadIdInCivi(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following SCAD IDs are "
                          "duplicated in CiviCRM: "),
            recipients=[RECIPIENT_SCAD_ADMIN],
            sql='''

SELECT  scad_id_58 AS scad_id
FROM STG_CiviCRM.dbo.civicrm_value_scad_15 scad
JOIN    STG_CiviCRM.dbo.civicrm_case cas
    ON cas.id = scad.entity_id
    AND cas.is_deleted = 0
    AND cas.status_id IN (5, 8)
    AND cas.case_type_id = 9
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
WHERE i2b2ClinDataIntegration.dbo.isNullOrEmpty(scad_id_58) = 0
GROUP BY scad_id_58
HAVING COUNT(*) > 1


                '''
        )

    def get_report_line(self, row):
        return "- **{}**\r\n".format(get_contact_id_search_link(
            row['scad_id'], row['scad_id']))
