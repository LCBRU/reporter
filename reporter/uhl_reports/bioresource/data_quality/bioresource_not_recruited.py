#!/usr/bin/env python3

from reporter.core import Schedule, SqlReport
from reporter.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.uhl_reports.civicrm import get_contact_id_search_link


class BioresourceConsentedNotRecruited(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants appear "
                          "to have full consent, but do not have a status "
                          "of recruited in CiviCRM"),
            recipients=[RECIPIENT_BIORESOURCE_ADMIN],
            sql='''

SELECT  CONVERT(VARCHAR(100), a.StudyNumber) as bioresource_id
    , a.consent_date
FROM    (
    SELECT  StudyNumber, consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval
    WHERE   full_consent = 1
    UNION
    SELECT  bioresource_id, NULL AS consent_date
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Redcap_Bioresource
    WHERE   full_consent = 1
) a
WHERE NOT EXISTS (
    SELECT  1
    FROM    i2b2_app03_bioresource_Data.dbo.LOAD_Civicrm_Interval i
    WHERE   (
					i.is_recruited = 1
                OR	i.is_excluded = 1
                OR	i.is_failed_to_respond = 1
                OR	i.is_declined = 1
                OR	i.is_duplicate = 1
				OR	i.is_withdrawn = 1
            ) AND (
				i.StudyNumber = a.StudyNumber
				OR (
					i.Legacy_Bioresource_ID = a.StudyNumber
					AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(i.Legacy_Bioresource_ID) = 0
				)
			)
		) AND NOT EXISTS (
			SELECT  1
			FROM [STG_CiviCRM].[dbo].[LCBRU_CaseDetails] d
			WHERE case_type_id = 7
			AND (
					d.is_recruited = 1
				OR	d.is_excluded = 1
				OR	d.is_failed_to_respond = 1
				OR	d.is_declined = 1
				OR	d.is_duplicate = 1
				OR	d.is_withdrawn = 1
			) AND (
					d.StudyNumber = a.StudyNumber
				OR (
						d.StudyNumber2 = a.StudyNumber
					AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(d.StudyNumber2) = 0
				)
			)
		)


                ''',
            schedule=Schedule.never,
        )

    def get_report_line(self, row):
        return '- {} {}\r\n'.format(
            get_contact_id_search_link(
                row['bioresource_id'], row['bioresource_id']),
            '{:%d-%b-%Y}'.format(row['consent_date'])
            if row['consent_date'] else ''
        )
