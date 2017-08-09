#!/usr/bin/env python3

from reporter.reports import PdfReport, Schedule
from reporter import RECIPIENT_BIORESOURCE_ADMIN


class BioresourceConsentFormIndex(PdfReport):
    def __init__(self):
        super().__init__(
            template='bioresource/management_information/consent_form_index.html',
            introduction=("Attached is the Bioresource Consent Form Index"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            schedule=Schedule.never,
            sql='''

SELECT
    YEAR(consent.consent_date) AS year,
    MONTH(consent.consent_date) AS month,
    DATENAME(MONTH, consent.consent_date) AS month_name,
    consent.consent_date,
    bio.[nihr_bioresource_id_41] AS StudyNumber,
    con.display_name
FROM (
    SELECT  bioresource_id AS bioresource_or_legacy_id, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource
    WHERE blank_study_id = 0
        AND consent_date IS NOT NULL
    UNION
    SELECT  bioresource_id, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval
    WHERE blank_study_id = 0
        AND consent_date IS NOT NULL
    UNION
    SELECT  bioresource_id, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_Bioresource
    WHERE consent_date IS NOT NULL
    UNION
    SELECT  bioresource_id, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_JointBriccs
    WHERE consent_date IS NOT NULL
) consent
JOIN    STG_CiviCRM.dbo.civicrm_value_nihr_bioresource_11 bio
    ON bio.[nihr_bioresource_id_41] = consent.bioresource_or_legacy_id
    OR bio.[nihr_bioresource_legacy_id_78] = consent.bioresource_or_legacy_id
JOIN    STG_CiviCRM.dbo.civicrm_case cas
    ON cas.id = bio.entity_id
    AND cas.is_deleted = 0
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
GROUP BY
    consent.consent_date,
    bio.[nihr_bioresource_id_41],
    con.last_name,
    con.first_name,
    con.display_name
ORDER BY
    YEAR(consent.consent_date),
    MONTH(consent.consent_date),
    con.last_name,
    con.first_name

                '''
        )


r = BioresourceConsentFormIndex()
r.run()
