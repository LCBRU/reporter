#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN


class FastMissingOrInvalidDataReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("Missing or invalid required data "
                          "in REDCap for FAST study"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''

WITH recruited AS (
    SELECT
        fast_id.record,
        fast_id.value AS fast_id
    FROM    STG_redcap.dbo.redcap_data recruited
    JOIN    STG_redcap.dbo.redcap_data fast_id
        ON fast_id.record = recruited.record
        AND fast_id.field_name = 'fst_label'
    WHERE recruited.project_id = 48
        AND recruited.field_name = 'patient_reruited'
        AND recruited.value = 1
)
SELECT
    r.fast_id,
    'Missing first name' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'first_name'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Missing last name' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'last_name'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Missing NHS Number' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'nhs_no'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Invalid NHS Number: ' + e.value AS [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'nhs_no'
    AND i2b2ClinDataIntegration.dbo.isInvalidNhsNumber(e.value) = 1
UNION
SELECT
    r.fast_id,
    'Missing Address' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM    STG_redcap.dbo.redcap_data ad
    WHERE   ad.project_id = 48
        AND ad.record = r.record
        AND ad.field_name LIKE 'add_[1-4]'
        AND LEN(RTRIM(LTRIM(ad.value))) > 0
)
UNION
SELECT
    r.fast_id,
    'Missing Postcode' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'postcode'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Invalid Postcode: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'postcode'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND i2b2ClinDataIntegration.dbo.isInvalidPostcode(e.value) = 1
UNION
SELECT
    r.fast_id,
    'Missing Gender' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 43
        AND e.record = r.record
        AND e.field_name = 'gender'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Invalid Email: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'email_add'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND i2b2ClinDataIntegration.dbo.isInvalidEmail(e.value) = 1
UNION
SELECT
    r.fast_id,
    'Missing Ethnicity' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 43
        AND e.record = r.record
        AND e.field_name = 'ethnicity'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Missing Date of Birth' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 43
        AND e.record = r.record
        AND e.field_name = 'dob'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Invalid Date of Birth: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'dob'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 0
UNION
SELECT
    r.fast_id,
    'Invalid Date of Birth: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'dob'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 1
    AND YEAR(e.value) < 1900
UNION
SELECT
    r.fast_id,
    'Missing Recruiting Practice Location' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'gp_practice'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Missing Clinic Date' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'clinic_date'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Invalid Clinic Date: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'clinic_date'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 0
UNION
SELECT
    r.fast_id,
    'Invalid Clinic Date: ' + e.value [error_message]
FROM recruited r
JOIN STG_redcap.dbo.redcap_data e
    ON e.project_id = 48
    AND e.record = r.record
    AND e.field_name = 'clinic_date'
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 1
    AND YEAR(e.value) < 1900
UNION
SELECT
    r.fast_id,
    'Missing Invitation Group' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'invitation_group'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Missing Invitation Type' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 43
        AND e.record = r.record
        AND e.field_name = 'invitation_type'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Patient attended flag not set' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'patient_attend'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Patient did not agree to scan' AS [error_message]
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM STG_redcap.dbo.redcap_data e
    WHERE e.project_id = 48
        AND e.record = r.record
        AND e.field_name = 'patient_agree_scan'
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
UNION
SELECT
    r.fast_id,
    'Invalid Study Number' [error_message]
FROM recruited r
WHERE i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(r.fast_id) = 1

ORDER BY fast_id

                '''
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for p in cursor:
            markdown += "- **{}** {}\r\n".format(
                p['fast_id'], p['error_message'])

        markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1
