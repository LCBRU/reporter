#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_contact_id_search_link, RECIPIENT_IT_DQ


class CivicrmSubjectDuplicateUhlSNumber(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following subjects have "
                          "a duplicate UHL System Number in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

SELECT  cid.uhl_s_number_2 [s_number]
FROM    STG_CiviCRM.dbo.civicrm_value_contact_ids_1 cid
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cid.entity_id
    AND con.is_deleted = 0
WHERE LEN(RTRIM(LTRIM(COALESCE(cid.uhl_s_number_2, '')))) > 0
GROUP BY cid.uhl_s_number_2 HAVING COUNT(*) > 1
;

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(row['s_number'], row['s_number'])
        )
