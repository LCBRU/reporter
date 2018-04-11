#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.reports.emailing import RECIPIENT_GENVASC_ADMIN
from reporter.reports.civicrm import get_case_link


class GenvascInvalidRecruitingPracticeCount(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following recruitments "
                          "do not have the appropriate number"
                          "of recruiting sites"),
            recipients=[RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.daily,
            sql='''

SELECT
    cas.civicrm_case_id,
    cas.civicrm_contact_id,
    cas.StudyNumber,
    COUNT(DISTINCT recruiting_gp_rel.contact_id_b) [recruiting_practices]
FROM STG_CiviCRM.[dbo].[LCBRU_CaseDetails] cas
LEFT JOIN   STG_CiviCRM.dbo.civicrm_relationship recruiting_gp_rel
    ON recruiting_gp_rel.case_id = cas.civicrm_case_id
    AND recruiting_gp_rel.relationship_type_id = 24 -- Recruiting Site
    AND COALESCE(recruiting_gp_rel.start_date, GETDATE()) <= GETDATE()
    AND COALESCE(recruiting_gp_rel.end_date, GETDATE()) > = GETDATE()
WHERE cas.case_type_id = 3 -- GENVASC
GROUP BY
    cas.civicrm_case_id,
    cas.civicrm_contact_id,
    cas.StudyNumber
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
