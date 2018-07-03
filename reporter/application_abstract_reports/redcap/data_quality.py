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
            conn=redcap_instance()['connection'],
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN redcap_metadata md
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
    FROM redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
ORDER BY pe.record

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields])),
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
            conn=redcap_instance()['connection'],
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN redcap_metadata md
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
    FROM redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
) AND EXISTS (
    SELECT 1
    FROM redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = %s
        AND e.value = %s
)
ORDER BY pe.record

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields])),
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
            conn=redcap_instance()['connection'],
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    redcap_data
    WHERE project_id = %s
)
SELECT
    r.project_id,
    r.record
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name IN ({0})
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
) AND EXISTS (
    SELECT 1
    FROM redcap_data e
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name = %s
        AND e.value = %s
)
ORDER BY r.record


                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields])),
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
    AND e.field_name IN ({0})

                '''.format(', '.join(['\'{}\''.format(f) for f in fields])),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.invalid_nhs_number(row['value']):
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
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM redcap_data e
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({0})
    AND i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(e.value) = 1

                '''.format(
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


class RedcapFieldMatchesRegularExpression(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        regular_expression,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        self._regular_expression = regular_expression
        super().__init__(
            introduction=("The following participants have an invalid "
                          "field in REDCap"),
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
    AND e.field_name IN ({0})

                '''.format(', '.join(['\'{}\''.format(f) for f in fields])),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if not re.search(self._regular_expression, row['value']):
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
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    e.project_id,
    e.record
FROM redcap_data e
WHERE e.project_id = %s
    AND i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(e.record) = 1
GROUP BY
    e.project_id,
    e.record

                ''',
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record'])
        )


class RedcapInvalidUhlSystemNumber(RedcapFieldMatchesRegularExpression):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):
        super().__init__(
            redcap_instance=redcap_instance,
            project_id=project_id,
            fields=fields,
            regular_expression='[A-Z]\d{7}',
            recipients=recipients,
            schedule=schedule,
        )


class RedcapInvalidPostCode(RedcapFieldMatchesRegularExpression):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):
        super().__init__(
            redcap_instance=redcap_instance,
            project_id=project_id,
            fields=fields,
            regular_expression='([A-Z][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][0-9][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][A-Z][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][A-Z][0-9][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][0-9][A-Z] [0-9][A-Z][A-Z])'
            '|([A-Z][A-Z][0-9][A-Z] [0-9][A-Z][A-Z])',
            recipients=recipients,
            schedule=schedule,
        )


class RedcapInvalidEmailAddress(RedcapFieldMatchesRegularExpression):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):
        super().__init__(
            redcap_instance=redcap_instance,
            project_id=project_id,
            fields=fields,
            regular_expression=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            recipients=recipients,
            schedule=schedule,
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
            introduction=("The following participants have an invalid "
                          "blood pressure in REDCap"),
            recipients=recipients,
            schedule=schedule,
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    p.project_id,
    p.record,
    sbp.value [sbp],
    dbp.value [dbp]
FROM (
    SELECT DISTINCT
        project_id,
        record
    FROM redcap_data
    WHERE project_id = %s
) p
LEFT JOIN redcap_data sbp
    ON sbp.project_id = p.project_id
    AND sbp.record = p.record
    AND sbp.field_name = %s
LEFT JOIN redcap_data dbp
    ON dbp.project_id = p.project_id
    AND dbp.record = p.record
    AND dbp.field_name = %s

                ''',
            parameters=(project_id, systolic_field_name, diastolic_field_name)
        )

    def get_report_line(self, row):
        error = self.get_error_message(row['sbp'], row['dbp'])

        if error:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                error
            )

    def get_error_message(self, sbp, dbp):
        if self.is_na(sbp) and self.is_na(dbp):
            return
        if sbp is None and dbp is None:
            return

        if sbp is None and dbp is not None:
            return 'Systolic BP not entered'
        if sbp is not None and dbp is None:
            return 'Diastolic BP not entered'
        if not sbp.replace('.', '', 1).isdigit():
            return 'Systolic BP is not numeric'
        if not dbp.replace('.', '', 1).isdigit():
            return 'Diastolic BP is not numeric'
        if float(sbp) > 200:
            return 'Systolic BP is too high'
        if float(dbp) < 35:
            return 'Diastolic BP is too low'
        if float(dbp) >= float(sbp):
            return 'Diastolic BP is above Systolic BP'

        return

    def is_na(self, value):
        return (value or '').strip().replace('/', '') == 'na'


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
    AND e.field_name IN ({})

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value):
        if (value or '').strip().replace('/', '') == 'na':
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 20 < float(value) < 200:
            return True


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
    AND e.field_name IN ({})

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value):
        if (value or '').strip().replace('/', '') == 'na':
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 100 < float(value) < 250:
            return True


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
    AND e.field_name IN ({})

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields])
            ),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value):
        if (value or '').strip().replace('/', '') == 'na':
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 1.0 < float(value) < 2.5:
            return True


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
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    e.project_id,
    e.record,
    md.element_label
FROM redcap_data e
JOIN redcap_metadata md
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
FROM redcap_data e
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
    AND md.element_type = 'text'
    AND md.element_validation_type LIKE 'date_%'
WHERE  e.project_id = %s
    AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
    AND ISDATE(e.value) = 1
    AND YEAR(e.value) < 1900

                ''',
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
            conn=redcap_instance()['connection'],
            sql='''

    SELECT
        p.project_id,
        p.record,
        feet.value [feet],
        inches.value [inches]
    FROM (
        SELECT DISTINCT
            project_id,
            record
        FROM    redcap_data
        WHERE project_id = %s
    ) p
    LEFT JOIN redcap_data feet
        ON feet.project_id = p.project_id
        AND feet.record = p.record
        AND feet.field_name = %s
    LEFT JOIN redcap_data inches
        ON inches.project_id = p.project_id
        AND inches.record = p.record
        AND inches.field_name = %s


                ''',
            parameters=(project_id, feet_field, inches_field)
        )

    def get_report_line(self, row):
        error = self.get_error_message(row['feet'], row['inches'])

        if error:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                error
            )

    def get_error_message(self, feet, inches):
        if self.is_na(feet) or self.is_na(inches):
            return
        if feet is None and inches is None:
            return

        if feet is None and inches is not None:
            return 'Height in feet not entered'
        if feet is not None and inches is None:
            return 'Height in inches not entered'
        if not feet.replace('.', '', 1).isdigit():
            return 'Height in feet is not numeric'
        if not inches.replace('.', '', 1).isdigit():
            return 'Height in inches is not numeric'
        if float(feet) < 3:
            return 'Height in feet too low'
        if float(feet) > 7:
            return 'Height in feet too high'
        if not 0 <= float(inches) < 12:
            return 'Height in inches is incorrect'

        return

    def is_na(self, value):
        return (value or '').strip().replace('/', '') == 'na'


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
    AND e.field_name IN ({})

                '''.format(', '.join(['\'{}\''.format(f) for f in fields])),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value):
        if (value or '').strip().replace('/', '') == 'na':
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 20.0 < float(value) < 200.0:
            return True


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
            conn=redcap_instance()['connection'],
            sql='''

    SELECT
        p.project_id,
        p.record,
        stones.value [stones],
        pounds.value [pounds]
    FROM (
        SELECT DISTINCT
            project_id,
            record
        FROM    redcap_data
        WHERE project_id = %s
    ) p
    LEFT JOIN redcap_data stones
        ON stones.project_id = p.project_id
        AND stones.record = p.record
        AND stones.field_name = %s
    LEFT JOIN redcap_data pounds
        ON pounds.project_id = p.project_id
        AND pounds.record = p.record
        AND pounds.field_name = %s


                ''',
            parameters=(project_id, stones_field, pounds_field)
        )

    def get_report_line(self, row):
        error = self.get_error_message(row['stones'], row['pounds'])

        if error:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                error
            )

    def get_error_message(self, stones, pounds):
        if self.is_na(stones) or self.is_na(pounds):
            return
        if stones is None and pounds is None:
            return

        if stones is not None and pounds is None:
            return 'Weight in pounds not entered'
        if not (stones or '0').replace('.', '', 1).isdigit():
            return 'Weight in stones is not numeric'
        if not pounds.replace('.', '', 1).isdigit():
            return 'Weight in pounds is not numeric'

        calculated_kg = ((float(stones or 0) * 14) + float(pounds)) * 0.453592

        if not 20.0 < calculated_kg < 200.0:
            return 'Invalid weight'

        return

    def is_na(self, value):
        return (value or '').strip().replace('/', '') == 'na'


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
    AND e.field_name IN ({})

                '''.format(', '.join(['\'{}\''.format(f) for f in fields])),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value):
        if (value or '').strip().replace('/', '') == 'na':
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 17.0 <= float(value) <= 80.0:
            return True


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
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    dob.project_id,
    dob.record,
    [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, rec.value)) AgeAtRecruitment
FROM    redcap_data dob
JOIN    redcap_data rec
    ON rec.project_id = dob.project_id
    AND rec.record = dob.record
    AND rec.field_name = %s
WHERE [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, rec.value)) NOT BETWEEN %s AND %s
    AND dob.field_name = %s
    AND dob.project_id = %s

                ''',
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
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    a.record,
    a.project_id
FROM    redcap_data a
WHERE a.project_id = %s
    AND a.field_name IN ({0})
    AND a.value IN ({1})
    AND {4} (
        SELECT 1
        FROM    redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ({2})
            AND b.value IN ({3})
    )

                '''.format(
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
            conn=redcap_instance_a()['connection'],
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
FROM    {0}.redcap_data a
JOIN    {0}.redcap_projects pa
    ON pa.project_id = @project_id_a
JOIN    {1}.redcap_projects pb
    ON pb.project_id = @project_id_b
LEFT JOIN {1}.redcap_data b
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
