#!/usr/bin/env python3

from reporter import RECIPIENT_TMAO_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport
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
