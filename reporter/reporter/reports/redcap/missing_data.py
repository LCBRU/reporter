#!/usr/bin/env python3

from reporter.reports import Report

# Abstract Reports


class RedcapMissingData(Report):
    def __init__(
        self, redcap_instance, project_id, fields, recipients, schedule=None
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
    JOIN STG_redcap.dbo.redcap_metadata md
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


class RedcapMissingDataWhen(Report):
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
    JOIN STG_redcap.dbo.redcap_metadata md
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


class RedcapInvalidNhsNumber(Report):
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
    AND i2b2ClinDataIntegration.dbo.isInvalidNhsNumber(e.value) = 1

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


class RedcapInvalidStudyNumber(Report):
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


class RedcapRecordInvalidStudyNumber(Report):
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


class RedcapInvalidUhlSystemNumber(Report):
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


class RedcapInvalidBloodPressure(Report):
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
    FROM    STG_redcap.dbo.redcap_data
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


class RedcapInvalidPulse(Report):
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


class RedcapInvalidHeightInCm(Report):
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


class RedcapInvalidDate(Report):
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
WHERE e.project_id = %s
    AND e.field_name IN ({1})
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
WHERE  e.project_id = %s
    AND e.field_name IN ({1})
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 1
    AND YEAR(e.value) < 1900

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id, project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )


class RedcapInvalidHeightInFeetAndInches(Report):
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


class RedcapInvalidWeightInKg(Report):
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


class RedcapInvalidWeightInStonesAndPounds(Report):
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


class RedcapInvalidBmi(Report):
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


class RedcapImpliesCheck(Report):
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
        FROM    STG_redcap.dbo.redcap_data b
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