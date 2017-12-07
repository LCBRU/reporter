#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    get_contact_id_search_link,
    get_case_link,
    get_contact_link
)

# Abstract Reports


class DuplicateStudyIdReport(Report):
    def __init__(self, case_type_id, recipients, schedule=None):
        super().__init__(
            introduction=("The following study IDs "
                          "have been duplicated in CiviCRM"),
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''
SELECT
    cd.case_type_id,
    cd.case_type_name,
    cd.StudyNumber
FROM STG_CiviCRM.dbo.LCBRU_CaseDetails cd
WHERE cd.case_status_id IN (
        5, --recruited
        8,  -- withdrawn
        6 -- Available for Cohort
    )
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(cd.StudyNumber) = 0
    AND cd.case_type_id = %s
GROUP BY
    cd.case_type_id,
    cd.case_type_name,
    cd.StudyNumber
HAVING COUNT(*) > 1

                ''',
            parameters=(case_type_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_id_search_link(
                row['StudyNumber'],
                row['StudyNumber']))


class MissingStudyNumber(Report):
    def __init__(self, case_type_id, recipients, schedule=None):
        super().__init__(
            introduction=("The following enrolments do not have "
                          "study numbers in CiviCRM"),
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''

SELECT
    cd.case_type_id,
    cd.civicrm_contact_id,
    cd.civicrm_case_id,
    cd.case_type_name
FROM STG_CiviCRM.dbo.LCBRU_CaseDetails cd
WHERE cd.case_status_id IN (
        5, --recruited
        8,  -- withdrawn
        6 -- Available for Cohort
    )
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(cd.StudyNumber) = 1
    AND cd.case_type_id = %s

                ''',
            parameters=(case_type_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['case_type_name'],
                row['civicrm_case_id'],
                row['civicrm_contact_id']))


class MultipleRecruitementsReport(Report):
    def __init__(self, case_type_id, recipients, schedule=None):
        super().__init__(
            introduction=("The following contacts have "
                          "multiple recruitments in CiviCRM"),
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''

SELECT
    cd.civicrm_contact_id,
    cd.case_type_name
FROM STG_CiviCRM.dbo.LCBRU_CaseDetails cd
WHERE cd.case_status_id IN (
        5, --recruited
        8,  -- withdrawn
        6 -- Available for Cohort
    )
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(cd.StudyNumber) = 0
    AND cd.case_type_id = %s
GROUP BY
    cd.civicrm_contact_id,
    cd.case_type_name
HAVING COUNT(*) > 1

                ''',
            parameters=(case_type_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(
                row['case_type_name'],
                row['civicrm_contact_id']))
