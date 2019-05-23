#!/usr/bin/env python3

from reporter.emailing import (
    RECIPIENT_PREECLAMPSIA_ADMIN as RECIPIENT_ADMIN
)
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)
from reporter.core import Schedule

CASE_TYPE_ID = 26


class PreeclampsiaCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class PreeclampsiaCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            case_type_id=CASE_TYPE_ID,
            valid_statuses=[
                'Recruited',
                'Excluded',
                'Withdrawn'
            ],
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )
