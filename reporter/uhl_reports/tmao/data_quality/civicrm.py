#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_TMAO_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    MissingUhlSystemNumberAndNhsNumberReport,
    CivicrmInvalidCaseStatus
)
from reporter.core import Schedule


CASE_TYPE_ID = 12


class TmaoCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_TMAO_ADMIN],
            schedule=Schedule.never,
        )


class TmaoCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_TMAO_ADMIN],
            schedule=Schedule.never,
        )


class TmaoCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_TMAO_ADMIN],
            schedule=Schedule.never,
        )


class TmaoCiviCrmMissingUhlNumberAndNhsNumber(
        MissingUhlSystemNumberAndNhsNumberReport):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            recipients=[RECIPIENT_TMAO_ADMIN],
            schedule=Schedule.never,
        )


class TmaoCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            CASE_TYPE_ID,
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_TMAO_ADMIN],
            schedule=Schedule.never,
        )
