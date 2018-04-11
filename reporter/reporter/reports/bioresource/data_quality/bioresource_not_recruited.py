#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.reports.civicrm import get_contact_id_search_link


class BioresourceConsentedNotRecruited(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants appear "
                          "to have full consent, but do not have a status "
                          "of recruited in CiviCRM"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT  CONVERT(VARCHAR(100), a.bioresource_id) as bioresource_id
    , a.consent_date
FROM    (
    SELECT  bioresource_id, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource
    WHERE   full_consent = 1
    UNION
    SELECT  bioresource_id, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval
    WHERE   full_consent = 1
    UNION
    SELECT  bioresource_id, NULL AS consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_Bioresource
    WHERE   full_consent = 1
    UNION
    SELECT  bioresource_id, NULL AS consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_JointBriccs
    WHERE   full_consent = 1
) a
WHERE   a.bioresource_id NOT IN (
    SELECT  bioresource_id
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource
    WHERE   (is_recruited = 1 OR is_excluded = 1 OR is_failed_to_respond = 1 OR is_declined = 1 OR is_duplicate = 1)
    UNION
    SELECT  bioresource_id
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval
    WHERE   (is_recruited = 1 OR is_excluded = 1 OR is_failed_to_respond = 1 OR is_declined = 1 OR is_duplicate = 1)
    UNION
    SELECT  legacy_bioresource_id
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Bioresource
    WHERE   (is_recruited = 1 OR is_excluded = 1 OR is_failed_to_respond = 1 OR is_declined = 1 OR is_duplicate = 1)
        AND LEN(RTRIM(LTRIM(ISNULL(legacy_bioresource_id, '')))) > 0
    UNION
    SELECT  legacy_bioresource_id
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval
    WHERE   (is_recruited = 1 OR is_excluded = 1 OR is_failed_to_respond = 1 OR is_declined = 1 OR is_duplicate = 1)
        AND LEN(RTRIM(LTRIM(ISNULL(legacy_bioresource_id, '')))) > 0
)

                '''
        )

    def get_report_line(self, row):
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row['bioresource_id'], row['bioresource_id']),
            '{:%d-%b-%Y}'.format(row['consent_date'])
            if row['consent_date'] else ''
        )
