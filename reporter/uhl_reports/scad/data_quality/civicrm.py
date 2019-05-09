#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.emailing import RECIPIENT_SCAD_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)
from reporter.uhl_reports.civicrm import (
    get_case_link,
)

CASE_TYPE_ID = 9

class ScadCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_SCAD_ADMIN])


class ScadCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_SCAD_ADMIN])


class ScadCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_SCAD_ADMIN])


class ScadCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            [
                'Recruited',
                'Excluded',
                'Duplicate',
                'Withdrawn',
                'Recruitment pending'
            ],
            [RECIPIENT_SCAD_ADMIN])


###
### Reg ID Column not yet available
###
#  
# class ScadCivicrmMissingRegId(SqlReport):
#     def __init__(self):
#         super().__init__(
#             introduction=("The following enrolments do not have "
#                           "SCAD Registry IDs in CiviCRM"),
#             recipients= [RECIPIENT_SCAD_ADMIN],
#             schedule=Schedule.daily,
#             sql='''

# SELECT
#     cd.case_type_id,
#     cd.civicrm_contact_id,
#     cd.civicrm_case_id,
#     cd.case_type_name
# FROM STG_CiviCRM.dbo.LCBRU_CaseDetails cd
# WHERE cd.case_status_id IN (
#         5, --recruited
#         8,  -- withdrawn
#         6 -- Available for Cohort
#     )
#     AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(cd.StudyNumber) = 1
#     AND cd.case_type_id = %s

#                 ''',
#             parameters=(CASE_TYPE_ID)
#         )

#     def get_report_line(self, row):
#         return '- {}\r\n'.format(
#             get_case_link(
#                 row['case_type_name'],
#                 row['civicrm_case_id'],
#                 row['civicrm_contact_id']))


