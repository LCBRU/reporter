#!/usr/bin/env python3

from reporter.reports.emailing import (
    RECIPIENT_SPIRAL_ADMIN as RECIPIENT_ADMIN
)
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)

CASE_TYPE_ID = 25


class SpiralCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN])


class SpiralCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN])


class SpiralCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN])


class SpiralCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            [
                'Recruited',
                'Excluded',
                'Withdrawn'
            ],
            [RECIPIENT_ADMIN])
