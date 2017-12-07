#!/usr/bin/env python3

from reporter import RECIPIENT_FAST_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport
)


class FastCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            18,
            recipients=[RECIPIENT_FAST_ADMIN])


class FastCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            18,
            recipients=[RECIPIENT_FAST_ADMIN])


class FastCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            18,
            recipients=[RECIPIENT_FAST_ADMIN])
