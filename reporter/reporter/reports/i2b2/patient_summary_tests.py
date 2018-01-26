#!/usr/bin/env python3

from reporter.reports import SqlReport
from reporter.reports.emailing import RECIPIENT_IT_DWH
from reporter.reports.civicrm import get_case_link, get_contact_link

# Abstract Reports


class PatientSummaryDuplicatesReport(SqlReport):
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


class PatientSummaryMissingData(SqlReport):
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


class PatientSummaryMissingParticipants(SqlReport):
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


class MissingNhsNumber(SqlReport):
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


class MissingDateOfBirth(SqlReport):
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


class MissingRecruitmentDate(SqlReport):
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


class MissingSampleFetchedDate(SqlReport):
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


class InvalidGender(SqlReport):
    def __init__(self, database, recipients, schedule=None):
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
