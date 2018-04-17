#!/usr/bin/env python3

from reporter.emailing import RECIPIENT_SCAD_ADMIN
from reporter.uhl_reports.civicrm.enrolment_dq import (
    DuplicateStudyIdReport,
    MissingStudyNumber,
    MultipleRecruitementsReport,
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
                'Withdrawn',
                'Recruitment pending'
            ],
            [RECIPIENT_SCAD_ADMIN])
