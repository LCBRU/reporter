from reporter.core import SqlReport, Schedule
from reporter.uhl_reports.civicrm import get_contact_id_search_link
from reporter.databases import DatabaseConnection


class PmiPatientMismatch(SqlReport):
    def __init__(self, project, recipients, schedule=None):
        super().__init__(
            introduction=('The following participant details do not match '
                          'the details in the UHL PMI'),
            conn=DatabaseConnection.dwbriccs,
            recipients=recipients,
            schedule=schedule or Schedule.daily,
            sql='''
                SELECT [StudyID]
                      ,[pmi_system_number]
                      ,[study_system_number]
                      ,[pmi_date_of_birth]
                      ,[study_date_of_birth]
                      ,[pmi_nhs_number]
                      ,[study_nhs_number]
                      ,[ProjectId]
                      ,[nhs_number_mismatch]
                      ,[date_of_birth_mismatch]
                      ,[system_number_missing]
                  FROM [DWBRICCS].[dbo].[LCBRU_Reports_PMI_Mismatch]
                  WHERE [ProjectId] = %s
                ''',
                parameters=(project)
        )

    def get_report_line(self, row):
        errors = []

        if row["system_number_missing"] == 1:
            errors.append('UHL System number not found')

        if row["nhs_number_mismatch"] == 1:
            errors.append(
                'NHS Number mismatch (Study=\'{}\'; PMI=\'{}\')'.format(
                    row['study_nhs_number'],
                    row['pmi_nhs_number']))

        if row["date_of_birth_mismatch"] == 1:
            errors.append(
                'DOB mismatch (Study=\'{}\'; PMI=\'{}\')'.format(
                    row['study_date_of_birth'],
                    row['pmi_date_of_birth']))

        return '- {}: {}\n'.format(
            get_contact_id_search_link(row["StudyID"], row["StudyID"]),
            '; '.join(errors)
        )
