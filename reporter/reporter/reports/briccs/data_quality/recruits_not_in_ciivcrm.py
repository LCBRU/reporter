#!/usr/bin/env python3

from reporter.reports import SqlReport
from reporter.reports.emailing import RECIPIENT_BRICCS_ADMIN


class BriccsNotInCivicrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_BRICCS_ADMIN],

            sql='''

SELECT  a.*
FROM i2b2_app03_b1_Data.dbo.Load_Fully_Consented a
WHERE NOT EXISTS (
    SELECT 1
    FROM i2b2_app03_b1_Data.dbo.LOAD_Civicrm b
    WHERE a.studynumber = b.studynumber
        AND (
            b.is_recruited = 1 OR
            b.is_excluded = 1 OR
            b.is_withdrawn = 1 OR
            b.is_duplicate = 1)
    )
    AND onyx_external = 0
    AND redcap_external_consent = 0

                '''
        )

    def get_report_line(self, row):
        consent_date = (
            '; Consent Date: {}'.format(row['consent_date_value'])
            if row['consent_date_value'] else '')

        consent_source = ''

        if row['civi_consent'] == 1:
            consent_source += '; consent in civicrm'
        if row['onyx_consent'] == 1:
            consent_source += '; consent in onyx'
        if row['redcap_consent'] == 1:
            consent_source += '; consent in redcap'
        if row['redcap_external_consent'] == 1:
            consent_source += '; consent in redcap external'

        return '- {}{}{}\r\n'.format(
            row['StudyNumber'],
            consent_date,
            consent_source)
