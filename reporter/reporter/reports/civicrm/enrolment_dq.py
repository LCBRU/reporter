#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.civicrm import (
    get_case_link,
    get_contact_id_search_link,
    get_contact_link
)


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


class MissingNhsNumberReport(Report):
    def __init__(self, case_type_id, recipients, schedule=None):
        super().__init__(
            introduction=("The following contacts do not have "
                          "an NHS Number in CiviCRM"),
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''

SELECT
    COALESCE(cd.StudyNumber, cd.case_type_name) StudyNumber,
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
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(NhsNumber) = 1

                ''',
            parameters=(case_type_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(
                row['StudyNumber'],
                row['civicrm_contact_id']))


class MissingUhlSystemNumberAndNhsNumberReport(Report):
    def __init__(self, case_type_id, recipients, schedule=None):
        super().__init__(
            introduction=("The following contacts do not have "
                          "an UHL System Number or an NHS Number"
                          "in CiviCRM"),
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''

SELECT
    COALESCE(cd.StudyNumber, cd.case_type_name) StudyNumber,
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
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(UhlSystemNumber) = 1
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(NhsNumber) = 1
                ''',
            parameters=(case_type_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(
                row['StudyNumber'],
                row['civicrm_contact_id']))


class CivicrmInvalidCaseStatus(Report):
    def __init__(self, case_type_id, valid_statuses, recipients):
        super().__init__(
            introduction=("The following cases have "
                          "invalid statuses:"),
            recipients=recipients,
            sql='''

SELECT
    cd.civicrm_contact_id,
    cd.civicrm_case_id,
    cd.case_status_name
FROM STG_CiviCRM.dbo.LCBRU_CaseDetails cd
WHERE cd.case_type_id = %s
    AND cd.case_status_name NOT IN ({})


                '''.format(','.join(['%s'] * len(valid_statuses))),
                parameters=tuple([case_type_id]) + tuple(valid_statuses),
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['case_status_name'],
                row['civicrm_case_id'],
                row['civicrm_contact_id']
            )
        )
