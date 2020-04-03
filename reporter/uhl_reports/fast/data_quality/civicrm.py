#!/usr/bin/env python3

from reporter.core import Schedule
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
            case_type_id=18,
            recipients=[RECIPIENT_FAST_ADMIN],
            schedule=Schedule.never,
        )


class FastCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            case_type_id=18,
            recipients=[RECIPIENT_FAST_ADMIN],
            schedule=Schedule.never,
        )


class FastCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            case_type_id=18,
            recipients=[RECIPIENT_FAST_ADMIN],
            schedule=Schedule.never,
        )


class FastCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            case_type_id=18,
            valid_statuses=[
                'Recruited',
                'Excluded',
                'Withdrawn',
                'Declined',
                'Duplicate',
            ],
            recipients=[RECIPIENT_FAST_ADMIN],
            schedule=Schedule.never,
        )
