#!/usr/bin/env python3

from reporter import RECIPIENT_INDAPAMIDE_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class IndapamideCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            19,
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN])


class IndapamideCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            19,
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN])


class IndapamideCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            19,
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN])


class IndapamideCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            19,
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_INDAPAMIDE_ADMIN])
