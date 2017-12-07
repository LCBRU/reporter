#!/usr/bin/env python3

from reporter import RECIPIENT_GENVASC_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    MissingNhsNumberReport
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