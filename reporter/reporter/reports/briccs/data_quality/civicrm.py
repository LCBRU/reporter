#!/usr/bin/env python3

from reporter.reports.emailing import RECIPIENT_BRICCS_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
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


class BriccsCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            6,
            recipients=[RECIPIENT_BRICCS_ADMIN])


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
