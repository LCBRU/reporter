#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    RECIPIENT_GENVASC_ADMIN, RECIPIENT_IT_DWH,
    get_contact_link, get_case_link)

# Abstract Reports


class PatientSummaryDuplicatesReport(Report):
    def __init__(self, database, schedule=None):
        super().__init__(
            introduction=("The following participants are duplicated "
                          "in the {} patient_summary view".format(database)),
            recipients=[RECIPIENT_IT_DWH],
            schedule=schedule,
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
    def __init__(self, database, fields, schedule=None):
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
            schedule=schedule,
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
    def __init__(self, database, schedule=None):
        super().__init__(
            introduction=("The following participants are "
                          "missing from the patient summary"),
            recipients=[RECIPIENT_IT_DWH],
            schedule=schedule,
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


class MissingNhsNumber(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants do "
                          "not have an NHS Number"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT [StudyNumber]
      ,[CiviCrmId]
FROM {}.[dbo].[PatientSummary]
WHERE RTRIM(LTRIM(LEN(COALESCE(NhsNumber, '')))) = 0
    AND IgnoreMissing = 'No'

                    '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link(
                row["StudyNumber"],
                row["CiviCrmId"]))


class MissingDateOfBirth(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants do "
                          "not have a Date of Birth"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT [StudyNumber]
      ,[CiviCrmId]
FROM {}.[dbo].[PatientSummary]
WHERE DateOfBirth IS NULL
    AND IgnoreMissing = 'No'

                    '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link(
                row["StudyNumber"],
                row["CiviCrmId"]))


class MissingRecruitmentDate(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants do "
                          "not have a Recruitment Date"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT [StudyNumber]
      ,[CiviCrmId]
FROM {}.[dbo].[PatientSummary]
WHERE RecruitmentDate IS NULL
    AND IgnoreMissing = 'No'

                    '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link(
                row["StudyNumber"],
                row["CiviCrmId"]))


class MissingSampleFetchedDate(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants do "
                          "not have a Sample Fetched Date"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT [StudyNumber]
      ,[CiviCrmId]
      ,[CiviCrmCaseId]
FROM {}.[dbo].[PatientSummary]
WHERE SampleFetchedDate IS NULL
    AND IgnoreMissing = 'No'

                    '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row["StudyNumber"],
                row["CiviCrmCaseId"],
                row["CiviCrmId"]))


class InvalidGender(Report):
    def __init__(self, database, recipients, schedule):
        super().__init__(
            introduction=("The following participants do "
                          "not have a valid gender"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT [StudyNumber]
      ,[CiviCrmId]
FROM i2b2_app03_genvasc_Data.[dbo].[PatientSummary]
WHERE LEFT(RTRIM(LTRIM(COALESCE(Gender, ''))), 1) NOT IN ('M', 'F', 'T')
    AND IgnoreMissing = 'No'

                    '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link(
                row["StudyNumber"],
                row["CiviCrmId"]))


# AS Progression

class AsProgressionPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            'i2b2_app03_ASProgression_Data',
            schedule=Schedule.never)


class AsProgressionPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_ASProgression_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'InterviewDate', 'Gender',
             'DateOfBirth', 'HeightAtInterview', 'WeightAtInterview'],
            schedule=Schedule.never
        )


class AsProgressionPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            'i2b2_app03_ASProgression_Data',
            schedule=Schedule.never)


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
        super().__init__(
            'i2b2_app03_b1_Data',
            schedule=Schedule.never)


class BriccsPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'InterviewDate', 'Gender', 'DateOfBirth',
             'HeightAtInterview', 'WeightAtInterview'],
            schedule=Schedule.never
        )


class BriccsPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            schedule=Schedule.never)


# GENVASC

class GenvascPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            schedule=Schedule.never)


class GenvascPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            ['CiviCrmId', 'StudyNumber', 'RecruitmentDate', 'Gender',
             'HeightAtRecruitment', 'WeightAtRecruitment', 'Ethnicity'],
            schedule=Schedule.never
        )


class GenavscPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            schedule=Schedule.never)


class GenvascMissingNhsNumber(
        MissingNhsNumber):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            [RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.never)


class GenvascMissingDateOfBirth(
        MissingDateOfBirth):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            [RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.never)


class GenvascMissingRecruitmentDate(
        MissingRecruitmentDate):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            [RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.never)


class GenvascMissingSampleFetchedDate(
        MissingSampleFetchedDate):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            [RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.never)


class GenvascInvalidGender(
        InvalidGender):
    def __init__(self):
        super().__init__(
            'i2b2_app03_genvasc_Data',
            [RECIPIENT_GENVASC_ADMIN],
            schedule=Schedule.never)


# GRAPHIC 2


class Graphic2PatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            'i2b2_app03_graphic2_Data',
            schedule=Schedule.never)


class Graphic2PatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_graphic2_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'DateOfInterview', 'Gender', 'DateOfBirth',
             'Height', 'Weight', 'Ethnicity'],
            schedule=Schedule.never
        )


class Graphic2PatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            'i2b2_app03_graphic2_Data',
            schedule=Schedule.never)


# OMICS


class OmicsPatientSummaryDuplicatesReport(
        PatientSummaryDuplicatesReport):
    def __init__(self):
        super().__init__(
            'i2b2_app03_omics_Data',
            schedule=Schedule.never)


class OmicsPatientSummaryMissingData(
        PatientSummaryMissingData):
    def __init__(self):
        super().__init__(
            'i2b2_app03_omics_Data',
            ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber',
             'StudyNumber', 'RecruitmentDateToSourceStudy',
             'Gender', 'DateOfBirth',
             'OmicsType', 'SourceStudy', 'Ethnicity'],
            schedule=Schedule.never
        )


class OmicsPatientSummaryMissingParticipants(
        PatientSummaryMissingParticipants):
    def __init__(self):
        super().__init__(
            'i2b2_app03_omics_Data',
            schedule=Schedule.never)
