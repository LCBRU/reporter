#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_BRICCS_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class BriccsCiviCrmDuplicateStudyIdReport(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            6,
            recipients=[RECIPIENT_BRICCS_ADMIN])


class BriccsCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            6,
            recipients=[RECIPIENT_BRICCS_ADMIN])


# Duplicates are allowed - Emma Beeston
# class BriccsCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
#     def __init__(self):
#         super().__init__(
#             6,
#             recipients=[RECIPIENT_BRICCS_ADMIN])


class BriccsCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            6,
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_BRICCS_ADMIN])
