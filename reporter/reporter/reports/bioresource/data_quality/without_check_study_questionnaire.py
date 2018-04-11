#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.reports.civicrm import get_case_link, get_contact_id_search_link
from reporter.emailing import RECIPIENT_BIORESOURCE_ADMIN


class BioresourceWithoutCheckStudyQuestionnaire(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants do not  "
                          "have a competed Check Study Questionnaire "
                          "activity in CiviCRM"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT
    rc. bioresource_id,
    CONVERT(DATE, REPLACE(rc.consent_date, '-', ''), 112) consent_date,
    civicrm_case_id,
    civicrm_contact_id
FROM [i2b2_app03_bioresource_Data].[dbo].[LOAD_Redcap_Bioresource] rc
LEFT JOIN [i2b2_app03_bioresource_Data].[dbo].[LOAD_Civicrm_Bioresource] cv
    ON (cv.bioresource_id = rc.bioresource_id
        OR cv.legacy_bioresource_id = rc.bioresource_id)
JOIN    STG_redcap.dbo.redcap_data rcq
    ON rcq.record = rc.bioresource_id
    AND rcq.field_name = 'recruitment_questionnaire_complete'
  WHERE NOT EXISTS (
        SELECT 1
        FROM STG_CiviCRM.dbo.civicrm_case cas
        JOIN STG_CiviCRM.dbo.civicrm_value_nihr_bioresource_11 bio
            ON bio.entity_id = cas.id
        JOIN STG_CiviCRM.dbo.civicrm_case_activity cas_act
            ON cas_act.case_id = cas.id
        JOIN    STG_CiviCRM.dbo.civicrm_activity act
            ON act.id = cas_act.activity_id
            AND act.activity_type_id = 76
            AND act.is_deleted = 0
            AND act.is_current_revision = 1
            AND act.status_id = 2
        WHERE cas.case_type_id = 7
            AND cas.is_deleted = 0
            AND (
                    bio.nihr_bioresource_id_41 = rc.bioresource_id
                OR bio.nihr_bioresource_legacy_id_78 = rc.bioresource_id
            )
    )

                '''
        )

    def get_report_line(self, row):
        if row['civicrm_case_id'] and row['civicrm_contact_id']:
            link = get_case_link(
                row['bioresource_id'],
                row["civicrm_case_id"],
                row["civicrm_contact_id"])
        else:
            link = get_contact_id_search_link(
                row["bioresource_id"],
                row["bioresource_id"])

        return '- {} Consent Date: {}\r\n'.format(
            link, row['consent_date'] or '')
