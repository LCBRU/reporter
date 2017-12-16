#!/usr/bin/env python3

from reporter.reports import PdfReport, Schedule
from reporter.reports.emailing import RECIPIENT_BIORESOURCE_ADMIN


class BioresourceQuestionnaireFormIndex(PdfReport):
    def __init__(self):
        super().__init__(
            template='bioresource/management_information/questionnaire_form_index.html',
            introduction=("Attached is the Bioresource Questionnaire Form Index"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            schedule=Schedule.never,
            sql='''

SELECT
    YEAR(act.activity_date_time) AS year,
    MONTH(act.activity_date_time) AS month,
    DATENAME(MONTH, act.activity_date_time) AS month_name,
    act.activity_date_time [check_questionnaire_date],
    bio.[nihr_bioresource_id_41] AS StudyNumber,
    con.display_name
FROM    STG_CiviCRM.dbo.civicrm_value_nihr_bioresource_11 bio
JOIN    STG_CiviCRM.dbo.civicrm_case cas
    ON cas.id = bio.entity_id
    AND cas.is_deleted = 0
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_case_activity cas_act
    ON cas_act.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_activity act
    ON act.id = cas_act.activity_id
    AND act.activity_type_id = 76 -- Check Study Questionnaire
    AND act.is_deleted = 0
    AND act.is_current_revision = 1
    AND act.status_id = 2 -- Completed
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
GROUP BY
    act.activity_date_time,
    bio.[nihr_bioresource_id_41],
    con.last_name,
    con.first_name,
    con.display_name
ORDER BY
    YEAR(act.activity_date_time),
    MONTH(act.activity_date_time),
    con.last_name,
    con.first_name

                '''
        )
