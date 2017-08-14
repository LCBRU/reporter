#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_contact_id_search_link, RECIPIENT_IT_DQ


class CivicrmSubjectDuplicateNhsNumber(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following subjects have "
                          "a duplicate NHS Number in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

SELECT  cid.nhs_number_1 [nhs_number]
FROM    STG_CiviCRM.dbo.civicrm_value_contact_ids_1 cid
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cid.entity_id
    AND con.is_deleted = 0
WHERE LEN(RTRIM(LTRIM(COALESCE(cid.nhs_number_1, '')))) > 0
GROUP BY cid.nhs_number_1 HAVING COUNT(*) > 1
;

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(row['nhs_number'], row['nhs_number'])
        )
