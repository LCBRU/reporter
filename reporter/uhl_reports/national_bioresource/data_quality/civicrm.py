#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_BIORESOURCE_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class NationalBioresourceCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            27,
            recipients=[RECIPIENT_BIORESOURCE_ADMIN])


class NationalBioresourceCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            27,
            recipients=[RECIPIENT_BIORESOURCE_ADMIN])


class NationalBioresourceCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            27,
            recipients=[RECIPIENT_BIORESOURCE_ADMIN])


class NationalBioresourceCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            27,
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
