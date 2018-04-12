#!/usr/bin/env python3

from reporter.emailing import (
    RECIPIENT_CARDIOMET_ADMIN as RECIPIENT_ADMIN
)
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)

CASE_TYPE_ID = 24


class CardiometCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN])


class CardiometCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN])


class CardiometCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN])


class CardiometCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            valid_statuses=[
                'Recruited',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            recipients=[RECIPIENT_ADMIN])
