#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.uhl_reports.civicrm import get_case_link
from reporter.uhl_reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
from reporter.uhl_reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
    PatientSummaryMissingDataWithMissingFlag,
)
from reporter.uhl_reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
    PatientSummaryMissingRecruited,
)
from reporter.emailing import (
    RECIPIENT_BRICCS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_IT_DWH,
)


I2B2_DB = "i2b2_app03_b1_Data"


# Duplicates are allowed - Emma Beeston
# class BriccsPatientMappingDuplicatesReport(
#         PatientMappingDuplicatesReport):
#     def __init__(self):
#         super().__init__(I2B2_DB)


class BriccsPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BriccsPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BriccsPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'NhsNumber',
                'ConsentDate',
                'StudyNumber',
                'InterviewDate',
                'Gender',
                'DateOfBirth',
            ]
        )


class BriccsPatientSummaryMissingHeight(
        PatientSummaryMissingDataWithMissingFlag):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            field='HeightAtInterview',
            missing_flag='height_not_recorded',
        )


class BriccsPatientSummaryMissingWeight(
        PatientSummaryMissingDataWithMissingFlag):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            field='WeightAtInterview',
            missing_flag='weight_not_recorded',
        )


class BriccsPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)

# Duplicates are allowed - Emma Beeston
# class BriccsValidEnrolmentsStudyIdDuplicates(
#         ValidEnrolmentsStudyIdDuplicates):
#     def __init__(self):
#         super().__init__(
#             I2B2_DB,
#             [RECIPIENT_ADMIN]
#         )


class BriccsValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class BriccsPatientSummaryMissingRecruited(
        PatientSummaryMissingRecruited):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )
