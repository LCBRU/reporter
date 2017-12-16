#!/usr/bin/env python3

from reporter.reports.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class BioresourceCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            7,
            recipients=[RECIPIENT_BIORESOURCE_ADMIN])


class BioresourceCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            7,
            recipients=[RECIPIENT_BIORESOURCE_ADMIN])


class BioresourceCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            7,
            recipients=[RECIPIENT_BIORESOURCE_ADMIN])


class BioresourceCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            7,
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_BIORESOURCE_ADMIN])


class BioresourceSubStudyCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            21,
            [
                'Recruited',
                'Available for cohort',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Withdrawn'
            ],
            [RECIPIENT_BIORESOURCE_ADMIN])
