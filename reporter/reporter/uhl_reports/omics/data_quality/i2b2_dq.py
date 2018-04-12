#!/usr/bin/env python3

from reporter.uhl_reports.i2b2.patient_mapping_tests import (
    PatientMappingDuplicatesReport,
    PatientMappingMultiplesIdsReport,
)
from reporter.uhl_reports.i2b2.patient_summary_tests import (
    PatientSummaryDuplicatesReport,
    PatientSummaryMissingData,
    PatientSummaryMissingParticipants,
)


class OmicsPatientMappingDuplicatesReport(
        PatientMappingDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_omics_Data')


class OmicsPatientMappingMultiplesIdsReport(
        PatientMappingMultiplesIdsReport):
    def __init__(self):
        super().__init__('i2b2_app03_omics_Data')


class OmicsPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            'i2b2_app03_omics_Data')


class OmicsPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_omics_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'RecruitmentDateToSourceStudy',
             'Gender', 'DateOfBirth',
             'OmicsType', 'SourceStudy', 'Ethnicity']
        )


class OmicsPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            'i2b2_app03_omics_Data')
