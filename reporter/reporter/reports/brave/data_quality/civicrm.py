#!/usr/bin/env python3

from reporter.reports.emailing import RECIPIENT_BRAVE_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class BraveCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            10,
            recipients=[RECIPIENT_BRAVE_ADMIN])


class BraveCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            10,
            recipients=[RECIPIENT_BRAVE_ADMIN])


class BraveCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            10,
            recipients=[RECIPIENT_BRAVE_ADMIN])


class BraveCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            10,
            [
                'Recruited',
                'Completed',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_BRAVE_ADMIN])
