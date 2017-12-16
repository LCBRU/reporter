#!/usr/bin/env python3

from reporter.reports.emailing import RECIPIENT_SCAD_ADMIN
from reporter.reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
    MissingNhsNumberReport,
    CivicrmInvalidCaseStatus
)


class ScadCiviCrmMissingStudyNumber(MissingStudyNumber):
    def __init__(self):
        super().__init__(
            9,
            recipients=[RECIPIENT_SCAD_ADMIN])


class ScadCiviCrmDuplicateStudyNumber(DuplicateStudyIdReport):
    def __init__(self):
        super().__init__(
            9,
            recipients=[RECIPIENT_SCAD_ADMIN])


class ScadCiviCrmMultipleRecruitments(MultipleRecruitementsReport):
    def __init__(self):
        super().__init__(
            9,
            recipients=[RECIPIENT_SCAD_ADMIN])


class ScadCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            9,
            [
                'Recruited',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_SCAD_ADMIN])
