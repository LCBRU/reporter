#!/usr/bin/env python3

from reporter.reports import Report
from reporter import (RECIPIENT_IT_DQ)


class DemographicsXrefMismatch(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are enrolled "
                          "in multiple studies, but their demographics"
                          "do not match: "),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

WITH matched_participants AS (
SELECT
    a.Study [a_study],
    b.Study [b_study],
    a.StudyId [a_study_id],
    b.StudyId [b_study_id],
    a.gender [a_gender],
    b.gender [b_gender],
    a.Birth_Date [a_birth_date],
    b.Birth_Date [b_birth_date],
    a.ethnicity [a_ethnicity],
    b.ethnicity [b_ethnicity]
FROM [i2b2ClinDataIntegration].[dbo].[all_participants] a
JOIN    [i2b2ClinDataIntegration].[dbo].[all_participants] b
    ON ((   b.NhsNumber = a.NhsNumber
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b.NhsNumber) = 0)
        OR (b.UhlSystemNumber = a.UhlSystemNumber
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b.UhlSystemNumber) = 0)
        OR (b.CiviCrmId = a.CiviCrmId AND b.CiviCrmId IS NOT NULL)
        )
    AND b.Study > a.Study
)

SELECT *, 'Birth Date Mismatch' [error_message]
FROM matched_participants
WHERE a_birth_date IS NOT NULL
    AND b_birth_date IS NOT NULL
    AND a_birth_date <> b_birth_date
UNION ALL
SELECT *, 'Gender Mismatch' [error_message]
FROM matched_participants
WHERE i2b2ClinDataIntegration.dbo.IsNullOrEmpty(a_gender) = 0
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b_gender) = 0
    AND a_gender <> b_gender
UNION ALL
SELECT *, 'Ethnicity Mismatch' [error_message]
FROM matched_participants
WHERE i2b2ClinDataIntegration.dbo.IsNullOrEmpty(a_ethnicity) = 0
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b_ethnicity) = 0
    AND a_ethnicity <> b_ethnicity
    AND a_ethnicity <> 'Z'
    AND b_ethnicity <> 'Z'
    AND NOT (a_ethnicity = 'A/B/C' AND b_ethnicity IN ('A', 'B', 'C'))
    AND NOT (b_ethnicity = 'A/B/C' AND a_ethnicity IN ('A', 'B', 'C'))

                '''
        )

    def get_report_line(self, row):
        result = '## {}: {} / {}: {} ({})\r\n\r\n'.format(
            row['a_study'],
            row['a_study_id'],
            row['b_study'],
            row['b_study_id'],
            row['error_message']
        )
        result += 'Date of Birth: {:%d %B %Y} / {:%d %B %Y}\r\n\r\n'.format(
            row['a_birth_date'],
            row['b_birth_date'],
        )
        result += 'Gender: {} / {}\r\n\r\n'.format(
            row['a_gender'],
            row['b_gender'],
        )
        result += 'Ethnicity: {} / {}\r\n\r\n'.format(
            row['a_ethnicity'],
            row['b_ethnicity'],
        )

        return result
