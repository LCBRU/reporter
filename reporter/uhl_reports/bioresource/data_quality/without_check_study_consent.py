#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.uhl_reports.civicrm import (
    get_case_link,
    get_contact_id_search_link,
)


class BioresourceWithoutCheckStudyConsent(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants do not  "
                          "have a competed Check Study Consent "
                          "activity in CiviCRM"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT
    rc.record bioresource_id,
    CONVERT(DATE, REPLACE(rc.date_of_sig, '-', ''), 112) consent_date,
    cv.civicrm_case_id,
    cv.civicrm_contact_id
FROM    (
        SELECT  record, field_name, value
        FROM    STG_redcap.dbo.redcap_data
        WHERE   project_id = 9
    ) p PIVOT
    (   MAX(value)
        FOR field_name in (
            consent_1,
            consent_2,
            consent_3,
            consent_4,
            consent_5,
            consent_6,
            date_of_sig,
            invalid_questionnaire_yn,
            excluded_yn
        )
    ) AS  rc
LEFT JOIN [i2b2_app03_bioresource_Data].[dbo].[LOAD_Civicrm_Bioresource] cv
    ON (cv.bioresource_id = rc.record
        OR cv.legacy_bioresource_id = rc.record)
WHERE
    rc.invalid_questionnaire_yn = 0
    AND COALESCE(excluded_yn, 0) = 0
    AND COALESCE(
        rc.consent_1,
        rc.consent_2,
        rc.consent_3,
        rc.consent_4,
        rc.consent_5,
        rc.consent_6) IS NOT NULL
    AND NOT EXISTS (
        SELECT 1
        FROM STG_CiviCRM.dbo.civicrm_case cas
        JOIN STG_CiviCRM.dbo.civicrm_value_nihr_bioresource_11 bio
            ON bio.entity_id = cas.id
        JOIN STG_CiviCRM.dbo.civicrm_case_activity cas_act
            ON cas_act.case_id = cas.id
        JOIN    STG_CiviCRM.dbo.civicrm_activity act
            ON act.id = cas_act.activity_id
            AND act.activity_type_id = 56
            AND act.is_deleted = 0
            AND act.is_current_revision = 1
            AND act.status_id = 2
        WHERE cas.case_type_id = 7
            AND cas.is_deleted = 0
            AND (
                    bio.nihr_bioresource_id_41 = rc.record
                OR bio.nihr_bioresource_legacy_id_78 = rc.record
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
