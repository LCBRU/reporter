#!/usr/bin/env python3

from reporter.core import Schedule
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
    PatientSummaryMissingDataWhen,
)
from reporter.uhl_reports.i2b2.valid_enrolment_tests import (
    ValidEnrolmentsStudyIdDuplicates,
    ValidEnrolmentsContactMultipleRecruitments,
    RecruitedWithoutFullConsent,
    PatientSummaryMissingRecruited,
)
from reporter.emailing import (
    RECIPIENT_FAST_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_IT_DWH,
)


I2B2_DB = "i2b2_app03_fast_Data"


class FastPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            schedule=Schedule.never,
        )


class FastPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            schedule=Schedule.never,
        )


class FastPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            schedule=Schedule.never,
        )


class FastPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            fields=[
                'NhsNumber',
                'StudyNumber',
                'CiviCrmId',
                'consent_date',
            ],
            schedule=Schedule.never,
        )


class FastPatientSummaryGenderMissingData(
    PatientSummaryMissingDataWhen):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            fields=['gender'],
            indicator_field='consent_ext_dta_coll',
            indicator_value='1',
            schedule=Schedule.never,
        )
    
    
class FastPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            schedule=Schedule.never,
        )


class FastValidEnrolmentsStudyIdDuplicates(
        ValidEnrolmentsStudyIdDuplicates):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastValidEnrolmentsContactMultipleRecruitments(
        ValidEnrolmentsContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastRecruitedWithoutFullConsent(
        RecruitedWithoutFullConsent):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastPatientSummaryMissingRecruited(
        PatientSummaryMissingRecruited):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )
