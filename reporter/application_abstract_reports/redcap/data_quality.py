#!/usr/bin/env python3

import re
from reporter.core import SqlReport

# Abstract Reports


class RedcapMissingData(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):
        self._redcap_instance = redcap_instance

        super().__init__(
            introduction=("The following participants have data "
                          "missing from REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    {1}.dbo.redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN {1}.dbo.redcap_metadata md
        ON md.project_id = r.project_id
        AND md.field_name IN ({0})
)
SELECT
    pe.project_id,
    pe.record,
    pe.error AS [error_message]
FROM potential_errors pe
WHERE NOT EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
ORDER BY pe.record

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields]),
                redcap_instance()['staging_database']),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )


class RedcapMissingDataWhen(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        indicator_field,
        indicator_value,
        recipients,
        schedule=None
    ):
        self._redcap_instance = redcap_instance

        super().__init__(
            introduction=("The following participants have data "
                          "missing from REDCap when {} = '{}'". format(
                              indicator_field,
                              indicator_value
                          )),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    {1}.dbo.redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN {1}.dbo.redcap_metadata md
        ON md.project_id = r.project_id
        AND md.field_name IN ({0})
)
SELECT
    pe.project_id,
    pe.record,
    pe.error AS [error_message]
FROM potential_errors pe
WHERE NOT EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
) AND EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = %s
        AND e.value = %s
)
ORDER BY pe.record

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields]),
                redcap_instance()['staging_database']),
            parameters=(project_id, indicator_field, indicator_value)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )


class RedcapMissingAllWhen(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        indicator_field,
        indicator_value,
        recipients,
        schedule=None
    ):
        self._redcap_instance = redcap_instance

        super().__init__(
            introduction=("The following participants have data "
                          "missing from REDCap when {} = '{}'". format(
                              indicator_field,
                              indicator_value
                          )),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    {1}.dbo.redcap_data
    WHERE project_id = %s
)
SELECT
    r.project_id,
    r.record
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name IN ({0})
        AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(e.value) = 0
) AND EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = %s
        AND e.value = %s
)
ORDER BY r.record


                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields]),
                redcap_instance()['staging_database']),
            parameters=(project_id, indicator_field, indicator_value)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']))


class RedcapInvalidNhsNumber(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid NHS Number "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    e.project_id,
    e.record,
    e.value,
    md.element_label
FROM redcap_data e
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_lines(self, cursor):
        markdown = ''
        errors = 0

        for row in cursor:
            if self.invalid_nhs_number(row['value']):
                markdown += self.get_report_line(row)
                errors += 1

        return markdown, errors

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )

    def invalid_nhs_number(self, nhs_number):
        """
            Checks a given NHS numbers <string> is valid.
            @Returns: is_valid<bool>
        """
        # Nhs number is sometimes inputted xxx-xxx-xxxx, lets strip this down
        nhs_number = re.sub('[- ]', '', nhs_number)

        # A valid NHS number must be 10 digits long
        if not re.search(r'^[0-9]{10}$', nhs_number):
            return False

        checkcalc = lambda sum: 11 - (sum % 11)

        char_total = sum(
            [int(j) * (11 - (i + 1)) for i, j in enumerate(nhs_number[:-1])]
        )
        checksum = checkcalc(char_total) if checkcalc(char_total) != 11 else 0

        return checksum != int(nhs_number[9])


class RedcapInvalidStudyNumber(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid study Number "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(e.value) = 1

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapRecordInvalidStudyNumber(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "study Number in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record
FROM {0}.dbo.redcap_data e
WHERE e.project_id = %s
    AND i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(e.record) = 1
GROUP BY
    e.project_id,
    e.record

                '''.format(
                redcap_instance()['staging_database']
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record'])
        )


class RedcapInvalidUhlSystemNumber(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid UHL S Number "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.isInvalidUhlSystemNumber(e.value) = 1

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidPostCode(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid post code "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.isInvalidPostcode(e.value) = 1

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidEmailAddress(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid "
                          "email address in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(e.value) = 0
    AND i2b2ClinDataIntegration.dbo.isInvalidEmail(e.value) = 1

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidBloodPressure(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        systolic_field_name,
        diastolic_field_name,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an blood pressure "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH participants AS (
    SELECT DISTINCT
        project_id,
        record
    FROM    {0}.dbo.redcap_data
    WHERE project_id = %s
), blood_pressures AS (
    SELECT
        p.project_id,
        p.record,
        sbp.value [sbp],
        dbp.value [dbp]
    FROM participants p
    LEFT JOIN {0}.dbo.redcap_data sbp
        ON sbp.project_id = p.project_id
        AND sbp.record = p.record
        AND sbp.field_name = %s
    LEFT JOIN {0}.dbo.redcap_data dbp
        ON dbp.project_id = p.project_id
        AND dbp.record = p.record
        AND dbp.field_name = %s
)
SELECT *
FROM (
    SELECT  *,
        CASE
            WHEN i2b2ClinDataIntegration.dbo.isNa(sbp) = 1
                OR i2b2ClinDataIntegration.dbo.isNa(dbp) = 1
                THEN NULL
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(sbp) = 1
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(dbp) = 1
                THEN NULL
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(sbp) = 1
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(dbp) = 0
                THEN 'Systolic BP not entered'
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(sbp) = 0
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(dbp) = 1
                THEN 'Diastolic BP not entered'
            WHEN i2b2ClinDataIntegration.dbo.IsReallyNumeric(sbp) = 0
                THEN 'Systolic BP not a number'
            WHEN i2b2ClinDataIntegration.dbo.IsReallyNumeric(dbp) = 0
                THEN 'Diastolic BP not a number'
            WHEN i2b2ClinDataIntegration.dbo.isInvalidBloodPressure(sbp,dbp) = 1
                THEN 'Invalid values for blood pressure'
        END [error_message]
    FROM    blood_pressures
) x
WHERE x.error_message IS NOT NULL
;
                '''.format(
                redcap_instance()['staging_database']
            ),
            parameters=(project_id, systolic_field_name, diastolic_field_name)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )


class RedcapInvalidPulse(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid Pulse "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.IsNa(e.value) = 0
    AND (i2b2ClinDataIntegration.dbo.IsReallyNumeric(e.value) = 0
        OR i2b2ClinDataIntegration.dbo.isInvalidPulse(e.value) = 1
        )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidHeightInCm(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "Height(cm) in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.IsNa(e.value) = 0
    AND (i2b2ClinDataIntegration.dbo.IsReallyNumeric(e.value) = 0
        OR i2b2ClinDataIntegration.dbo.isInvalidHeightInCm(e.value) = 1
        )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidHeightInM(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "Height(m) in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.IsNa(e.value) = 0
    AND (i2b2ClinDataIntegration.dbo.IsReallyNumeric(e.value) = 0
        OR i2b2ClinDataIntegration.dbo.isInvalidHeightInCm(e.value * 100) = 1
        )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidDate(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid Date "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
    AND md.element_type = 'text'
    AND md.element_validation_type LIKE 'date_%'
WHERE e.project_id = %s
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 0
UNION
SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
    AND md.element_type = 'text'
    AND md.element_validation_type LIKE 'date_%'
WHERE  e.project_id = %s
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 1
    AND YEAR(e.value) < 1900

                '''.format(
                redcap_instance()['staging_database'],
            ),
            parameters=(project_id, project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidHeightInFeetAndInches(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        feet_field,
        inches_field,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "Height(feet and inches) in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH participants AS (
    SELECT DISTINCT
        project_id,
        record
    FROM    {0}.dbo.redcap_data
    WHERE project_id = %s
), heights AS (
    SELECT
        p.project_id,
        p.record,
        feet.value [feet],
        inches.value [inches]
    FROM participants p
    LEFT JOIN {0}.dbo.redcap_data feet
        ON feet.project_id = p.project_id
        AND feet.record = p.record
        AND feet.field_name = %s
    LEFT JOIN {0}.dbo.redcap_data inches
        ON inches.project_id = p.project_id
        AND inches.record = p.record
        AND inches.field_name = %s
)
SELECT *
FROM (
    SELECT  *,
        CASE
            WHEN i2b2ClinDataIntegration.dbo.isNa(feet) = 1
                OR i2b2ClinDataIntegration.dbo.isNa(inches) = 1
                THEN NULL
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(feet) = 1
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(feet) = 1
                THEN NULL
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(feet) = 1
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(inches) = 0
                THEN 'Height in feet not entered'
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(feet) = 0
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(inches) = 1
                THEN 'Height in inches not entered'
            WHEN i2b2ClinDataIntegration.dbo.IsReallyNumeric(feet) = 0
                THEN 'Height in feet not a number'
            WHEN i2b2ClinDataIntegration.dbo.IsReallyNumeric(inches) = 0
                THEN 'Height in inches not a number'
            WHEN i2b2ClinDataIntegration.dbo.isInvalidHeightInFeetAndInches(feet,inches) = 1
                THEN 'Invalid values for Height in feet and inches'
        END [error_message]
    FROM    heights
) x
WHERE x.error_message IS NOT NULL
;

                '''.format(
                redcap_instance()['staging_database']
            ),
            parameters=(project_id, feet_field, inches_field)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )


class RedcapInvalidWeightInKg(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "Weight(kg) in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.IsNa(e.value) = 0
    AND (i2b2ClinDataIntegration.dbo.IsReallyNumeric(e.value) = 0
        OR i2b2ClinDataIntegration.dbo.isInvalidWeightInKg(e.value) = 1
        )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidWeightInStonesAndPounds(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        stones_field,
        pounds_field,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "Weight(Stones and pounds) in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH participants AS (
    SELECT DISTINCT
        project_id,
        record
    FROM    {0}.dbo.redcap_data
    WHERE project_id = %s
), weights AS (
    SELECT
        p.project_id,
        p.record,
        stones.value [stones],
        pounds.value [pounds]
    FROM participants p
    LEFT JOIN {0}.dbo.redcap_data stones
        ON stones.project_id = p.project_id
        AND stones.record = p.record
        AND stones.field_name = %s
    LEFT JOIN {0}.dbo.redcap_data pounds
        ON pounds.project_id = p.project_id
        AND pounds.record = p.record
        AND pounds.field_name = %s
)
SELECT *
FROM (
    SELECT  *,
        CASE
            WHEN i2b2ClinDataIntegration.dbo.isNa(stones) = 1
                OR i2b2ClinDataIntegration.dbo.isNa(pounds) = 1
                THEN NULL
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(stones) = 1
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(pounds) = 1
                THEN NULL
            WHEN i2b2ClinDataIntegration.dbo.isNullOrEmpty(stones) = 0
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(pounds) = 1
                THEN 'Weight in pounds not entered'
            WHEN i2b2ClinDataIntegration.dbo.IsReallyNumeric(stones) = 0
                AND i2b2ClinDataIntegration.dbo.isNullOrEmpty(stones) = 0
                THEN 'Weight in stones not a number'
            WHEN i2b2ClinDataIntegration.dbo.IsReallyNumeric(pounds) = 0
                THEN 'Weight in pounds not a number'
            WHEN i2b2ClinDataIntegration.dbo.isInvalidWeightInStonesAndPounds(stones,pounds) = 1
                THEN 'Invalid values for Weight in stones and pounds'
        END [error_message]
    FROM    weights
) x
WHERE x.error_message IS NOT NULL
;

                '''.format(
                redcap_instance()['staging_database']
            ),
            parameters=(project_id, stones_field, pounds_field)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )


class RedcapInvalidBmi(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants have an invalid "
                          "BMI in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM {0}.dbo.redcap_data e
JOIN {0}.dbo.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({1})
    AND i2b2ClinDataIntegration.dbo.IsNa(e.value) = 0
    AND (i2b2ClinDataIntegration.dbo.IsReallyNumeric(e.value) = 0
        OR i2b2ClinDataIntegration.dbo.isInvalidBmi(e.value) = 1
        )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapOutsideAgeRange(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        dob_field,
        recruited_date_field,
        min_age,
        max_age,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants were recruited "
                          "outside the specified age range witin REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    dob.project_id,
    dob.record,
    [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, rec.value)) AgeAtRecruitment
FROM    {0}.dbo.redcap_data dob
JOIN    {0}.dbo.redcap_data rec
    ON rec.project_id = dob.project_id
    AND rec.record = dob.record
    AND rec.field_name = %s
WHERE [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, rec.value)) NOT BETWEEN %s AND %s
    AND dob.field_name = %s
    AND dob.project_id = %s

                '''.format(
                redcap_instance()['staging_database'],
            ),
            parameters=(
                recruited_date_field,
                min_age,
                max_age,
                dob_field,
                project_id,
            )
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['AgeAtRecruitment']
        )


class RedcapImpliesCheck(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        indicator_fields,
        indicator_values,
        consequence_fields,
        consequence_values,
        error_message,
        recipients,
        reverse=False,
        schedule=None
    ):
        self._redcap_instance = redcap_instance
        self._error_message = error_message

        if reverse:
            comparison = "EXISTS"
        else:
            comparison = "NOT EXISTS"

        super().__init__(
            introduction=("The following participants have the following "
                          "invalid data in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    a.record,
    a.project_id
FROM    {0}.dbo.redcap_data a
WHERE a.project_id = %s
    AND a.field_name IN ({1})
    AND a.value IN ({2})
    AND {5} (
        SELECT 1
        FROM    {0}.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ({3})
            AND b.value IN ({4})
    )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['%s'] * len(indicator_fields)),
                ', '.join(['%s'] * len(indicator_values)),
                ', '.join(['%s'] * len(consequence_fields)),
                ', '.join(['%s'] * len(consequence_values)),
                comparison
            ),
            parameters=(tuple([project_id]) + tuple(indicator_fields) +
                        tuple(indicator_values) + tuple(consequence_fields) +
                        tuple(consequence_values))
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            self._error_message
        )


class RedcapXrefMismatch(SqlReport):
    def __init__(
        self,
        redcap_instance_a,
        project_id_a,
        field_name_a,
        redcap_instance_b,
        project_id_b,
        field_name_b,
        recipients,
        schedule=None
    ):

        self._redcap_instance_a = redcap_instance_a
        self._redcap_instance_b = redcap_instance_b

        super().__init__(
            introduction=("The following fields do not match "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

DECLARE @project_id_a INT,
        @project_id_b INT,
        @field_name_a VARCHAR(100),
        @field_name_b VARCHAR(100)

SELECT  @project_id_a = %s,
        @project_id_b = %s,
        @field_name_a = %s,
        @field_name_b = %s

SELECT
    a.record,
    @field_name_a [field_name_a],
    @field_name_b [field_name_b],
    @project_id_a [project_id_a],
    @project_id_b [project_id_b],
    pa.app_title [project_title_a],
    pb.app_title [project_title_b]
FROM    {0}.dbo.redcap_data a
JOIN    {0}.dbo.redcap_projects pa
    ON pa.project_id = @project_id_a
JOIN    {1}.dbo.redcap_projects pb
    ON pb.project_id = @project_id_b
LEFT JOIN {1}.dbo.redcap_data b
    ON b.project_id = @project_id_b
        AND b.field_name = @field_name_b
        AND b.record = a.record
WHERE a.project_id = @project_id_a
    AND a.field_name = @field_name_a
    AND COALESCE(a.value, '') <> COALESCE(b.value, '')


                '''.format(
                redcap_instance_a()['staging_database'],
                redcap_instance_b()['staging_database'],
            ),
            parameters=(
                project_id_a,
                project_id_b,
                field_name_a,
                field_name_b,
            )
        )

    def get_report_line(self, row):
        return '- {}: {} <> {}\r\n'.format(
            row['record'],
            self._redcap_instance_a()['link_generator'](
                '{}({})'.format(
                    row['project_title_a'],
                    row['field_name_a'],
                ),
                row['project_id_a'],
                row['record']),
            self._redcap_instance_a()['link_generator'](
                '{}({})'.format(
                    row['project_title_b'],
                    row['field_name_b'],
                ),
                row['project_id_b'],
                row['record']),
        )
