#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import RECIPIENT_IT_DWH


class BriccsNotInCivicrm(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants have "
                          "a record in REDCap, but do not have "
                          "a record in CiviCRM"),
            recipients=[RECIPIENT_IT_DWH],

            sql='''

SELECT	StudyNumber, consent_date, 'REDCap UHL' AS source
FROM	i2b2_app03_b1_Data.dbo.LOAD_Redcap
WHERE BlankStudyNumber = 0
	AND StudyNumber NOT IN (
		SELECT StudyNumber
		FROM i2b2_app03_b1_Data.dbo.LOAD_Civicrm b
		WHERE (
				b.is_recruited = 1 OR
				b.is_excluded = 1 OR
				b.is_withdrawn = 1 OR
				b.is_duplicate = 1)
			AND StudyNumber IS NOT NULL
	)

UNION

SELECT	StudyNumber, consent_date, 'Onyx' AS source
FROM	i2b2_app03_b1_Data.dbo.LOAD_Onyx
WHERE BlankStudyNumber = 0
	AND RecruitingSite = 'briccs_glenfield_recruitment'
	AND StudyNumber NOT IN (
		SELECT StudyNumber
		FROM i2b2_app03_b1_Data.dbo.LOAD_Civicrm b
		WHERE (
				b.is_recruited = 1 OR
				b.is_excluded = 1 OR
				b.is_withdrawn = 1 OR
				b.is_duplicate = 1)
			AND StudyNumber IS NOT NULL
	)

                '''
        )

    def get_report_line(self, row):
        consent_date = (
            '; Consent Date: {}'.format(row['consent_date'])
            if row['consent_date'] else '')

        consent_source = ''

        return '- {}{}; {}\r\n'.format(
            row['StudyNumber'],
            consent_date,
            row['source'])
