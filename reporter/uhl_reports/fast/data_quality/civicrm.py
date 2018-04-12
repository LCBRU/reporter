#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_FAST_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class FastCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            18,
            recipients=[RECIPIENT_FAST_ADMIN])


class FastCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            18,
            recipients=[RECIPIENT_FAST_ADMIN])


class FastCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            18,
            recipients=[RECIPIENT_FAST_ADMIN])


class FastCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            18,
            [
                'Recruited',
                'Excluded',
                'Withdrawn'
            ],
            [RECIPIENT_FAST_ADMIN])
