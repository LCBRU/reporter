#!/usr/bin/env python3

from reporter.reports import Report
from reporter import RECIPIENT_IT_DWH

FIELDS = ['CiviCrmId', 'NhsNumber', 'UhlSystemNumber', 'BioresourceId',
          'StudyNumber', 'EnrolmentDate', 'ConsentDate', 'Gender', 'DOB',
          'DateOfBirth', 'Height', 'Weight']


class BioresourcePatientSummaryMissingData(Report):
    def __init__(self):
        selects = map(
            (lambda x:
                'CASE WHEN {0} IS NULL THEN 1 ELSE 0 END [{0}]'.format(x)),
            FIELDS)
        wheres = map(
            (lambda x:
                '{0} IS NULL'.format(x)),
            FIELDS)
        super().__init__(
            introduction=("The following participants are duplicated "
                          "in the patient_summary view"),
            recipients=[RECIPIENT_IT_DWH],
            sql='''
                SELECT
                    patient_num,
                    StudyNumber [ID],
                    {}
                FROM i2b2_app03_bioresource_Data.dbo.PatientSummary ps
                WHERE
                    ({})
                    AND invalid_questionnaire = 'No'
                    AND questionnaire_validated = 'No'
                '''.format(', '.join(selects), ' OR '.join(wheres))
        )

    def get_report_line(self, row):
        missing_fields = [f for f in FIELDS if row[f] == 1]

        return '- {} ({}): {}\r\n'.format(
            row['ID'],
            row['patient_num'],
            ', '.join(missing_fields)
        )
