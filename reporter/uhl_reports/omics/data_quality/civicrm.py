#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.uhl_reports.civicrm import get_contact_link
from reporter.emailing import RECIPIENT_IT_DQ


class OmicsButNoOtherStudy(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following contacts have an OMICS registration "
                          "but are not recruited into any other study in CiviCRM."),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

SELECT civicrm_contact_id
FROM STG_CiviCRM.dbo.LCBRU_CaseDetails
WHERE case_type_id = 14 --OMICS
	AND (is_recruited = 1 OR is_available_to_cohort = 1)
	AND civicrm_contact_id NOT IN (
		SELECT DISTINCT civicrm_contact_id
		FROM STG_CiviCRM.dbo.LCBRU_CaseDetails
		WHERE case_type_id <> 14 -- Not OMICS
			AND (is_recruited = 1 OR is_available_to_cohort = 1)
	);

                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link('Click here to see contact', row['contact_id'])
        )
