#!/usr/bin/env python3

from reporter.reports import Report
from reporter import RECIPIENT_IT_DWH

# Abstract Reports


class PatientSummaryDuplicatesReport(Report):
    def __init__(self, database):
        super().__init__(
            introduction=("The following participants are duplicated "
                          "in the {} patient_summary view".format(database)),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                SELECT patient_num, COUNT(*) AS ct
                FROM    {}.dbo.PatientSummary
                GROUP BY patient_num
                HAVING COUNT(*) > 1;
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['patient_num'])


class PatientSummaryMissingData(Report):
    def __init__(self, database, fields):
        self.fields = fields

        selects = map(
            (lambda x:
                'CASE WHEN {0} IS NULL THEN 1 ELSE 0 END [{0}]'.format(x)),
            self.fields)
        wheres = map(
            (lambda x:
                '{0} IS NULL'.format(x)),
            self.fields)
        super().__init__(
            introduction=("The following participants have data "
                          "missing from the patient_summary view"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                SELECT
                    patient_num,
                    StudyNumber [ID],
                    {}
                FROM {}.dbo.PatientSummary ps
                WHERE
                    ({})
                    AND IgnoreMissing = 'No'
                '''.format(', '.join(selects), database, ' OR '.join(wheres))
        )

    def get_report_line(self, row):
        missing_fields = [f for f in self.fields if row[f] == 1]

        return '- {} ({}): {}\r\n'.format(
            row['ID'],
            row['patient_num'],
            ', '.join(missing_fields)
        )


class PatientSummaryMissingParticipants(Report):
    def __init__(self, database):
        super().__init__(
            introduction=("The following participants are "
                          "missing from the patient summary"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                SELECT pd.Patient_Num
                FROM {0}.dbo.Patient_Dimension pd
                WHERE pd.Patient_Num NOT IN (
                    SELECT ps.Patient_Num
                    FROM {0}.dbo.PatientSummary ps)
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(row['patient_num'])


# AS Progression

class AsProgressionPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_ASProgression_Data')


class AsProgressionPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_ASProgression_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'InterviewDate', 'Gender',
             'DateOfBirth', 'HeightAtInterview', 'WeightAtInterview']
        )


class AsProgressionPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__('i2b2_app03_ASProgression_Data')


# Bioresource

class BioresourcePatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_bioresource_Data')


class BioresourcePatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_bioresource_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'BioresourceId', 'StudyNumber', 'EnrolmentDate',
             'ConsentDate', 'Gender', 'DOB', 'DateOfBirth',
             'Height', 'Weight']
        )


class BioresourcePatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__('i2b2_app03_bioresource_Data')


# BRICCS

class BriccsPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_b1_Data')


class BriccsPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'InterviewDate', 'Gender', 'DateOfBirth',
             'HeightAtInterview', 'WeightAtInterview']
        )


# GENVASC

class GenvascPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_genvasc_Data')


class GenvascPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'RecruitmentDate', 'Gender', 'DateOfBirth',
             'HeightAtRecruitment', 'WeightAtRecruitment', 'Ethnicity']
        )


class GenavscPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__('i2b2_app03_genvasc_Data')


# GRAPHIC 2


class Graphic2PatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_graphic2_Data')


class Graphic2PatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_graphic2_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'DateOfInterview', 'Gender', 'DateOfBirth',
             'Height', 'Weight', 'Ethnicity']
        )


class Graphic2PatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__('i2b2_app03_graphic2_Data')


# OMICS


class OmicsPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__('i2b2_app03_omics_Data')


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
        super().__init__('i2b2_app03_omics_Data')
