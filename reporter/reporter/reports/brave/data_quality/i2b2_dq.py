#!/usr/bin/env python3

from reporter.reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
)
from reporter.reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
)
from reporter.reports.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
)


I2B2_DB = "i2b2_app03_brave_Data"


class BravePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BravePatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'NhsNumber',
                'UhlSystemNumber',
                'StudyNumber',
                'Gender',
                'DateOfBirth',
            ]
        )


class BravePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)


class BraveValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class BraveValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )
