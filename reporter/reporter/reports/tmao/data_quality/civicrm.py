#!/usr/bin/env python3

from reporter import RECIPIENT_TMAO_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    MissingUhlSystemNumberAndNhsNumberReport,
    CivicrmInvalidCaseStatus
)


class TmaoCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            12,
            recipients=[RECIPIENT_TMAO_ADMIN])


class TmaoCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            12,
            recipients=[RECIPIENT_TMAO_ADMIN])


class TmaoCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            12,
            recipients=[RECIPIENT_TMAO_ADMIN])


class TmaoCiviCrmMissingUhlNumberAndNhsNumber(
        MissingUhlSystemNumberAndNhsNumberReport):
    def __init__(self):
        super().__init__(
            12,
            recipients=[RECIPIENT_TMAO_ADMIN])


class TmaoCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            10,
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_TMAO_ADMIN])


r = TmaoCivicrmInvalidCaseStatus()
r.run()
