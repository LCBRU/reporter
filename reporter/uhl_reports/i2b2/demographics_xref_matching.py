#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.emailing import (RECIPIENT_IT_DQ)


class DemographicsXrefMismatch(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following participants are enrolled "
                          "in multiple studies, but their demographics"
                          "do not match: "),
            recipients=[RECIPIENT_IT_DQ],
            sql='''

CREATE TABLE #participants
(
	NhsNumber VARCHAR(200),
	blank_NhsNumber BIT,
	UhlSystemNumber VARCHAR(200),
	blank_UhlSystemNumber BIT,
	CiviCrmId VARCHAR(200),
	blank_CiviCrmId BIT,
    Study VARCHAR(14),
    StudyId VARCHAR(200),
    gender VARCHAR(MAX),
    gender_first_char VARCHAR(1),
    Birth_Date DATETIME,
    ethnicity VARCHAR(MAX)
)

INSERT INTO #participants (
	NhsNumber,
	blank_NhsNumber,
	UhlSystemNumber,
	blank_UhlSystemNumber,
	CiviCrmId,
	blank_CiviCrmId,
	Study,
	StudyId,
	gender,
	gender_first_char,
	Birth_Date,
	ethnicity
)
SELECT
	NhsNumber,
	CASE WHEN i2b2ClinDataIntegration.dbo.IsNullOrEmpty(NhsNumber) = 1 THEN 1 ELSE 0 END,
	UhlSystemNumber,
	CASE WHEN i2b2ClinDataIntegration.dbo.IsNullOrEmpty(UhlSystemNumber) = 1 THEN 1 ELSE 0 END,
	CiviCrmId,
	CASE WHEN CiviCrmId IS NOT NULL THEN 1 ELSE 0 END,
	Study,
	StudyId,
	gender,
	LEFT(gender, 1),
	Birth_Date,
	ethnicity
FROM [i2b2ClinDataIntegration].[dbo].[all_participants] a

CREATE INDEX idx_participants_NhsNumber ON #participants (NhsNumber, Study);
CREATE INDEX idx_participants_UhlSystemNumber ON #participants (UhlSystemNumber, Study);
CREATE INDEX idx_participants_CiviCrmId ON #participants (CiviCrmId, Study);

CREATE TABLE #xref
(
    a_study VARCHAR(14),
    a_study_id VARCHAR(200),
    a_gender VARCHAR(MAX),
	a_gender_first_char VARCHAR(1),
    a_birth_date DATETIME,
    a_ethnicity VARCHAR(MAX),
    b_study VARCHAR(14),
    b_study_id VARCHAR(200),
    b_gender VARCHAR(MAX),
	b_gender_first_char VARCHAR(1),
    b_birth_date DATETIME,
    b_ethnicity VARCHAR(MAX)
)
INSERT INTO #xref (
    a_Study,
    a_Study_id,
    a_gender,
	a_gender_first_char,
    a_Birth_Date,
    a_ethnicity,
    b_Study,
    b_Study_id,
    b_gender,
	b_gender_first_char,
    b_Birth_Date,
    b_ethnicity
)
SELECT
    a.Study [a_study],
    a.StudyId [a_study_id],
    a.gender [a_gender],
	a.gender_first_char [a_gender_first_char],
    a.Birth_Date [a_birth_date],
    a.ethnicity [a_ethnicity],
    b.Study [b_study],
    b.StudyId [b_study_id],
    b.gender [b_gender],
	b.gender_first_char [b_gender_first_char],
    b.Birth_Date [b_birth_date],
    b.ethnicity [b_ethnicity]
FROM #participants a
JOIN    #participants b
	ON b.NhsNumber = a.NhsNumber
	AND b.blank_NhsNumber = 0
	AND b.Study > a.Study
UNION
SELECT
    a.Study [a_study],
    a.StudyId [a_study_id],
    a.gender [a_gender],
	a.gender_first_char [a_gender_first_char],
    a.Birth_Date [a_birth_date],
    a.ethnicity [a_ethnicity],
    b.Study [b_study],
    b.StudyId [b_study_id],
    b.gender [b_gender],
	b.gender_first_char [b_gender_first_char],
    b.Birth_Date [b_birth_date],
    b.ethnicity [b_ethnicity]
FROM #participants a
JOIN    #participants b
	ON b.UhlSystemNumber = a.UhlSystemNumber
	AND b.blank_UhlSystemNumber = 0
	AND b.Study > a.Study
UNION
SELECT
    a.study [a_study],
    a.studyId [a_study_id],
    a.gender [a_gender],
	a.gender_first_char [a_gender_first_char],
    a.Birth_Date [a_birth_date],
    a.ethnicity [a_ethnicity],
    b.Study [b_study],
    b.StudyId [b_study_id],
    b.gender [b_gender],
	b.gender_first_char [b_gender_first_char],
    b.Birth_Date [b_birth_date],
    b.ethnicity [b_ethnicity]
FROM #participants a
JOIN    #participants b
	ON b.CiviCrmId = a.CiviCrmId
	AND b.blank_CiviCrmId = 0
	AND b.Study > a.Study

SELECT *, 'Birth Date Mismatch' [error_message]
FROM #xref
WHERE a_birth_date IS NOT NULL
    AND b_birth_date IS NOT NULL
    AND a_birth_date <> b_birth_date
UNION ALL
SELECT *, 'Gender Mismatch' [error_message]
FROM #xref
WHERE i2b2ClinDataIntegration.dbo.IsNullOrEmpty(a_gender) = 0
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b_gender) = 0
    AND a_gender_first_char <> b_gender_first_char
UNION ALL
SELECT *, 'Ethnicity Mismatch' [error_message]
FROM #xref
WHERE i2b2ClinDataIntegration.dbo.IsNullOrEmpty(a_ethnicity) = 0
    AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b_ethnicity) = 0
    AND a_ethnicity <> b_ethnicity
    AND a_ethnicity <> 'Z'
    AND b_ethnicity <> 'Z'
    AND NOT (a_ethnicity = 'White' AND b_ethnicity LIKE '%white%')
    AND NOT (b_ethnicity = 'White' AND a_ethnicity LIKE '%white%')

DROP TABLE #participants;
DROP TABLE #xref;


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
        if row['a_birth_date']:
            a_birth_date_str = '{:%d %B %Y}'.format(row['a_birth_date'])
        else:
            a_birth_date_str = '[NULL]'
        if row['b_birth_date']:
            b_birth_date_str = '{:%d %B %Y}'.format(row['b_birth_date'])
        else:
            b_birth_date_str = '[NULL]'

        result += 'Date of Birth: {} / {}\r\n\r\n'.format(
            a_birth_date_str,
            b_birth_date_str,
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
