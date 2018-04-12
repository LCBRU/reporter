#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_PREDICT_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    CivicrmInvalidCaseStatus
)


class PredictCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            23,
            recipients=[RECIPIENT_PREDICT_ADMIN])


class PredictCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            23,
            recipients=[RECIPIENT_PREDICT_ADMIN])


class PredictCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            23,
            recipients=[RECIPIENT_PREDICT_ADMIN])


class PredictCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            23,
            [
                'Recruited',
                'Excluded',
                'Withdrawn'
            ],
            [RECIPIENT_PREDICT_ADMIN])
