#!/usr/bin/env python3

from reporter.uhl_reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
)
from reporter.uhl_reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
)
from reporter.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
)
from reporter.core import Schedule


I2B2_DB = "i2b2_app03_brave_Data"


class BravePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(database=I2B2_DB)


# Cannot differentiate external participants who would not have these fields
class BravePatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            fields=[
                'CiviCrmId',
                'NhsNumber',
                'UhlSystemNumber',
                'StudyNumber',
                'Sex',
                'DateOfBirth',
            ],schedule=Schedule.never,        )


class BravePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(database=I2B2_DB)


class BraveValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_ADMIN]
        )


class BraveValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_ADMIN],
        )
