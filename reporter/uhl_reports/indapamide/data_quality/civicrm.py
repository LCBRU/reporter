#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_INDAPAMIDE_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)
from reporter.core import Schedule


class IndapamideCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            19,
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN],
            schedule=Schedule.never,
        )


class IndapamideCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            19,
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN],
            schedule=Schedule.never,
        )


class IndapamideCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            19,
            recipients=[RECIPIENT_INDAPAMIDE_ADMIN],
            schedule=Schedule.never,
        )


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
            [RECIPIENT_INDAPAMIDE_ADMIN],
            schedule=Schedule.never,
        )
