#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_case_link, RECIPIENT_GENVASC_ADMIN


class GenvascInvalidRecruitingPracticeCount(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following recruitments "
                          "do not have the appropriate number"
                          "of recruiting sites"),
            recipients=[RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.daily,
            sql='''

SELECT
    cas.id [civicrm_case_id],
    cas_con.contact_id [civicrm_contact_id],
    gen.genvasc_id_10 [StudyNumber],
    COUNT(DISTINCT recruiting_gp_rel.contact_id_b) [recruiting_practices]
FROM    STG_CiviCRM.dbo.civicrm_case cas
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_value_genvasc_recruitment_data_5 gen
    ON gen.entity_id = cas.id
LEFT JOIN   STG_CiviCRM.dbo.civicrm_relationship recruiting_gp_rel
    ON recruiting_gp_rel.case_id = cas.id
    AND recruiting_gp_rel.relationship_type_id = 24 -- Recruiting Site
    AND COALESCE(recruiting_gp_rel.start_date, GETDATE()) <= GETDATE()
    AND COALESCE(recruiting_gp_rel.end_date, GETDATE()) > = GETDATE()
WHERE cas.case_type_id = 3 -- GENVASC
    AND cas.is_deleted = 0
GROUP BY
    cas.id,
    cas_con.contact_id,
    gen.genvasc_id_10
HAVING COUNT(DISTINCT recruiting_gp_rel.contact_id_b) <> 1

                '''
        )

    def get_report_line(self, row):
        return '- {}: {} recruiting sites\r\n\r\n'.format(
            get_case_link(
                row["StudyNumber"],
                row["civicrm_case_id"],
                row["civicrm_contact_id"]),
            row["recruiting_practices"])
