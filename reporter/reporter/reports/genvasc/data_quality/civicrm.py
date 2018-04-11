#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_GENVASC_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    MissingNhsNumberReport,
    CivicrmInvalidCaseStatus
)


class GenvascCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            3,
            recipients=[RECIPIENT_GENVASC_ADMIN])


class GenvascCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            3,
            recipients=[RECIPIENT_GENVASC_ADMIN])


class GenvascCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            3,
            recipients=[RECIPIENT_GENVASC_ADMIN])


class GenvascCiviCrmMissingNhsNumber(MissingNhsNumberReport):
    def __init__(self):
        super().__init__(
            3,
            recipients=[RECIPIENT_GENVASC_ADMIN])


class GenvascCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            3,
            [
                'Available for cohort',
                'Recruited',
                'Excluded',
                'Withdrawn'
            ],
            [RECIPIENT_GENVASC_ADMIN])
