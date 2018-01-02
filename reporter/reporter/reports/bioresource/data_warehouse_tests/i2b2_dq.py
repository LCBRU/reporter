#!/usr/bin/env python3

from reporter.reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
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
    RECIPIENT_BIORESOURCE_ADMIN as RECIPIENT_ADMIN,
)


I2B2_DB = "i2b2_app03_bioresource_Data"


class BioresourcePatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourcePatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourcePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourcePatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [
                'CiviCrmId',
                'NhsNumber',
                'UhlSystemNumber',
                'BioresourceId',
                'StudyNumber',
                'EnrolmentDate',
                'ConsentDate',
                'Gender',
                'DOB',
                'DateOfBirth',
                'Height',
                'Weight',
            ]
        )


class BioresourcePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(I2B2_DB)


class BioresourceValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )


class BioresourceValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_ADMIN]
        )
