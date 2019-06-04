#!/usr/bin/env python3

import re
import datetime
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
    SELECT  DISTINCT rd.record, rd.project_id
    FROM    redcap_data rd
    WHERE project_id = %s
		AND NOT EXISTS (
			SELECT 1
			FROM redcap_data stat
			WHERE stat.project_id = rd.project_id
				AND stat.record = rd.record
				AND stat.field_name IN ('study_status_comp_yn', 'study_status')
				AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
			)
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
	LEFT JOIN redcap_data_quality_status dqs
		ON dqs.project_id = r.project_id
		AND dqs.record = r.record
		AND dqs.field_name = md.field_name
	LEFT JOIN redcap_data_quality_resolutions dqr
		ON dqr.status_id = dqs.status_id
		AND (
                dqr.comment LIKE 'valid'
            OR  dqr.comment LIKE 'valid %%'
            OR  dqr.comment LIKE '%% valid'
            OR  dqr.comment LIKE '%% valid %%'
            OR	dqr.comment LIKE 'validated'
            OR	dqr.comment LIKE 'validated %%'
            OR  dqr.comment LIKE '%% validated'
            OR  dqr.comment LIKE '%% validated %%'
        )
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
    SELECT  DISTINCT rd.record, rd.project_id
    FROM    redcap_data rd
    WHERE project_id = %s
		AND NOT EXISTS (
			SELECT 1
			FROM redcap_data stat
			WHERE stat.project_id = rd.project_id
				AND stat.record = rd.record
				AND stat.field_name IN ('study_status_comp_yn', 'study_status')
				AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
			)
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
	LEFT JOIN redcap_data_quality_status dqs
		ON dqs.project_id = r.project_id
		AND dqs.record = r.record
		AND dqs.field_name = md.field_name
	LEFT JOIN redcap_data_quality_resolutions dqr
		ON dqr.status_id = dqs.status_id
		AND (
                dqr.comment LIKE 'valid'
            OR  dqr.comment LIKE '%% valid'
            OR  dqr.comment LIKE 'valid %%'
            OR  dqr.comment LIKE '%% valid %%'
            OR	dqr.comment LIKE 'validated'
            OR	dqr.comment LIKE 'validated %%'
            OR  dqr.comment LIKE '%% validated'
            OR  dqr.comment LIKE '%% validated %%'
        )
	WHERE dqr.res_id IS NULL
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


class RedcapMissingDataWhenNot(SqlReport):
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
                          "missing from REDCap when {} not = '{}'". format(
                              indicator_field,
                              indicator_value
                          )),
            recipients=recipients,
            schedule=schedule,
            conn=redcap_instance()['connection'],
            sql='''

WITH recruited AS (
    SELECT  DISTINCT rd.record, rd.project_id
    FROM    redcap_data rd
    WHERE project_id = %s
		AND NOT EXISTS (
			SELECT 1
			FROM redcap_data stat
			WHERE stat.project_id = rd.project_id
				AND stat.record = rd.record
				AND stat.field_name IN ('study_status_comp_yn', 'study_status')
				AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
			)
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
	LEFT JOIN redcap_data_quality_status dqs
		ON dqs.project_id = r.project_id
		AND dqs.record = r.record
		AND dqs.field_name = md.field_name
	LEFT JOIN redcap_data_quality_resolutions dqr
		ON dqr.status_id = dqs.status_id
		AND (
                dqr.comment LIKE 'valid'
            OR  dqr.comment LIKE 'valid %%'
            OR  dqr.comment LIKE '%% valid'
            OR  dqr.comment LIKE '%% valid %%'
            OR	dqr.comment LIKE 'validated'
            OR	dqr.comment LIKE 'validated %%'
            OR  dqr.comment LIKE '%% validated'
            OR  dqr.comment LIKE '%% validated %%'
        )
	WHERE dqr.res_id IS NULL
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
        AND e.value <> %s
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
    SELECT  DISTINCT rd.record, rd.project_id
    FROM    redcap_data rd
    WHERE project_id = %s
		AND NOT EXISTS (
			SELECT 1
			FROM redcap_data stat
			WHERE stat.project_id = rd.project_id
				AND stat.record = rd.record
				AND stat.field_name IN ('study_status_comp_yn', 'study_status')
				AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
			)
)
SELECT
    r.project_id,
    r.record
FROM recruited r
WHERE NOT EXISTS (
    SELECT 1
    FROM redcap_data e
	LEFT JOIN redcap_data_quality_status dqs
		ON dqs.project_id = e.project_id
		AND dqs.record = e.record
		AND dqs.field_name = e.field_name
	LEFT JOIN redcap_data_quality_resolutions dqr
		ON dqr.status_id = dqs.status_id
		AND (
                dqr.comment LIKE 'valid'
            OR  dqr.comment LIKE '%% valid'
            OR  dqr.comment LIKE 'valid %%'
            OR  dqr.comment LIKE '%% valid %%'
            OR	dqr.comment LIKE 'validated'
            OR	dqr.comment LIKE 'validated %%'
            OR  dqr.comment LIKE '%% validated'
            OR  dqr.comment LIKE '%% validated %%'
        )
    WHERE e.project_id = r.project_id
        AND e.record = r.record
        AND e.field_name IN ({0})
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
        AND dqr.res_id IS NULL
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
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({0})
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

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

SELECT DISTINCT
    e.project_id,
    e.record,
    md.element_label
FROM redcap_data e
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({0})
    AND i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(e.value) = 1
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

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
    md.element_label,
    e.field_name
FROM redcap_data e
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ({0})
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )
ORDER BY e.record

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
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE e.project_id = %s
    AND i2b2ClinDataIntegration.dbo.isInvalidStudyNumber(e.record) = 1
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )
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
            regular_expression='[A-Za-z]\d{7}',
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
            regular_expression='(?i)([A-Z][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][0-9][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][A-Z][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][A-Z][0-9][0-9] [0-9][A-Z][A-Z])'
            '|([A-Z][0-9][A-Z] [0-9][A-Z][A-Z])'
            '|([A-Z][A-Z][0-9][A-Z] [0-9][A-Z][A-Z])|(^$)',
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
            regular_expression=r"(^|[a-zA-Z0-9'_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)|(^[nN]o email$)",
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
    sbp.value AS sbp,
    dbp.value AS dbp,
    CASE WHEN sbp_dqr.res_id IS NULL THEN 0 ELSE 1 END sbp_validated,
    CASE WHEN dbp_dqr.res_id IS NULL THEN 0 ELSE 1 END dbp_validated
FROM (
    SELECT DISTINCT
        project_id,
        record
    FROM redcap_data e
    WHERE project_id = %s
        AND NOT EXISTS (
            SELECT 1
            FROM redcap_data stat
            WHERE stat.project_id = e.project_id
                AND stat.record = e.record
                AND stat.field_name IN ('study_status_comp_yn', 'study_status')
                AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
            )
) p
LEFT JOIN redcap_data sbp
    ON sbp.project_id = p.project_id
    AND sbp.record = p.record
    AND sbp.field_name = %s
LEFT JOIN redcap_data dbp
    ON dbp.project_id = p.project_id
    AND dbp.record = p.record
    AND dbp.field_name = %s
LEFT JOIN redcap_data_quality_status sbp_dqs
    ON sbp_dqs.project_id = sbp.project_id
    AND sbp_dqs.record = sbp.record
    AND sbp_dqs.field_name = sbp.field_name
LEFT JOIN redcap_data_quality_resolutions sbp_dqr
    ON sbp_dqr.status_id = sbp_dqs.status_id
    AND (
            sbp_dqr.comment LIKE 'valid'
        OR  sbp_dqr.comment LIKE 'valid %%'
        OR  sbp_dqr.comment LIKE '%% valid'
        OR  sbp_dqr.comment LIKE '%% valid %%'
        OR	sbp_dqr.comment LIKE 'validated'
        OR	sbp_dqr.comment LIKE 'validated %%'
        OR  sbp_dqr.comment LIKE '%% validated'
        OR  sbp_dqr.comment LIKE '%% validated %%'
    )
LEFT JOIN redcap_data_quality_status dbp_dqs
    ON dbp_dqs.project_id = sbp.project_id
    AND dbp_dqs.record = sbp.record
    AND dbp_dqs.field_name = sbp.field_name
LEFT JOIN redcap_data_quality_resolutions dbp_dqr
    ON dbp_dqr.status_id = dbp_dqs.status_id
    AND (
            dbp_dqr.comment LIKE 'valid'
        OR  dbp_dqr.comment LIKE '%% valid'
        OR  dbp_dqr.comment LIKE 'valid %%'
        OR  dbp_dqr.comment LIKE '%% valid %%'
        OR	dbp_dqr.comment LIKE 'validated'
        OR	dbp_dqr.comment LIKE 'validated %%'
        OR  dbp_dqr.comment LIKE '%% validated'
        OR  dbp_dqr.comment LIKE '%% validated %%'
    )

                ''',
            parameters=(project_id, systolic_field_name, diastolic_field_name)
        )

    def get_report_line(self, row):
        error = self.get_error_message(row['sbp'], row['dbp'], row['sbp_validated'], row['dbp_validated'])

        if error:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                error
            )

    def get_error_message(self, sbp, dbp, sbp_validated, dbp_validated):
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
        if float(sbp) > 200 and sbp_validated == 0:
            return 'Systolic BP is too high'
        if float(dbp) < 35 and dbp_validated == 0:
            return 'Diastolic BP is too low'
        if float(dbp) >= float(sbp):
            return 'Diastolic BP is above Systolic BP'

        return

    def is_na(self, value):
        return (value or '').strip().replace('/', '').lower() == 'na'


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
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE e.project_id = %s
    AND e.field_name IN ({})
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

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
        if (value or '').strip().replace('/', '').lower() == 'na':
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
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE e.project_id = %s
    AND e.field_name IN ({})
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

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
        if (value or '').strip().replace('/', '').lower() == 'na':
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
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE e.project_id = %s
    AND e.field_name IN ({})
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

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
        if (value or '').strip().replace('/', '').lower() == 'na':
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
    e.value,
    md.element_label,
    md.element_validation_type
FROM redcap_data e
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
    AND md.element_type = 'text'
    AND md.element_validation_type LIKE 'date_%%'
WHERE e.project_id = %s
    AND e.value IS NOT NULL
    AND REPLACE(e.value, ' ', '') <> ''
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

                ''',
            parameters=(project_id)
        )

    def get_report_line(self, row):
        invalid = 1

        if row['element_validation_type'][:5] == 'date_':
            invalid = self.is_invalid(row['value'], '%Y-%m-%d')
        elif row['element_validation_type'][:9] == 'datetime_':
            invalid = self.is_invalid(row['value'], '%Y-%m-%d %H:%M')

        if invalid:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value, format_string):
        try:
            datetime.datetime.strptime(value, format_string)
            return 0
        except ValueError:
            return 1


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
        inches.value [inches],
        CASE WHEN feet_dqr.res_id IS NULL THEN 0 ELSE 1 END feet_validated
    FROM (
        SELECT DISTINCT
            project_id,
            record
        FROM    redcap_data e
        WHERE project_id = %s
            AND NOT EXISTS (
                SELECT 1
                FROM redcap_data stat
                WHERE stat.project_id = e.project_id
                    AND stat.record = e.record
                    AND stat.field_name IN ('study_status_comp_yn', 'study_status')
                    AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
                )
    ) p
    LEFT JOIN redcap_data feet
        ON feet.project_id = p.project_id
        AND feet.record = p.record
        AND feet.field_name = %s
    LEFT JOIN redcap_data inches
        ON inches.project_id = p.project_id
        AND inches.record = p.record
        AND inches.field_name = %s
    LEFT JOIN redcap_data_quality_status feet_dqs
        ON feet_dqs.project_id = feet.project_id
        AND feet_dqs.record = feet.record
        AND feet_dqs.field_name = feet.field_name
    LEFT JOIN redcap_data_quality_resolutions feet_dqr
        ON feet_dqr.status_id = feet_dqs.status_id
        AND (
                feet_dqr.comment LIKE 'valid'
            OR  feet_dqr.comment LIKE 'valid %%'
            OR  feet_dqr.comment LIKE '%% valid'
            OR  feet_dqr.comment LIKE '%% valid %%'
            OR	feet_dqr.comment LIKE 'validated'
            OR	feet_dqr.comment LIKE 'validated %%'
            OR  feet_dqr.comment LIKE '%% validated'
            OR  feet_dqr.comment LIKE '%% validated %%'
        )
                ''',
            parameters=(project_id, feet_field, inches_field)
        )

    def get_report_line(self, row):
        error = self.get_error_message(row['feet'], row['inches'], row['feet_validated'])

        if error:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                error
            )

    def get_error_message(self, feet, inches, feet_validated):
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
        if float(feet) < 3 and feet_validated == 0:
            return 'Height in feet too low'
        if float(feet) > 7 and feet_validated == 0:
            return 'Height in feet too high'
        if not 0 <= float(inches) < 12:
            return 'Height in inches is incorrect'

        return

    def is_na(self, value):
        return (value or '').strip().replace('/', '').lower() == 'na'


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
    md.element_label,
    CASE WHEN dqr.res_id IS NULL THEN 0 ELSE 1 END validated
FROM redcap_data e
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE e.project_id = %s
    AND e.field_name IN ({})
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

                '''.format(', '.join(['\'{}\''.format(f) for f in fields])),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value'], row['validated']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value, validated):
        if (value or '').strip().replace('/', '').lower() == 'na':
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 20.0 < float(value) < 200.0 and validated == 0:
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
        pounds.value [pounds],
        CASE WHEN stones_dqr.res_id IS NULL THEN 0 ELSE 1 END stones_validated
    FROM (
        SELECT DISTINCT
            project_id,
            record
        FROM    redcap_data e
        WHERE project_id = %s
            AND NOT EXISTS (
                SELECT 1
                FROM redcap_data stat
                WHERE stat.project_id = e.project_id
                    AND stat.record = e.record
                    AND stat.field_name IN ('study_status_comp_yn', 'study_status')
                    AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
                )
    ) p
    LEFT JOIN redcap_data stones
        ON stones.project_id = p.project_id
        AND stones.record = p.record
        AND stones.field_name = %s
    LEFT JOIN redcap_data pounds
        ON pounds.project_id = p.project_id
        AND pounds.record = p.record
        AND pounds.field_name = %s
    LEFT JOIN redcap_data_quality_status stones_dqs
        ON stones_dqs.project_id = stones.project_id
        AND stones_dqs.record = stones.record
        AND stones_dqs.field_name = stones.field_name
    LEFT JOIN redcap_data_quality_resolutions stones_dqr
        ON stones_dqr.status_id = stones_dqs.status_id
        AND (
                stones_dqr.comment LIKE 'valid'
            OR  stones_dqr.comment LIKE 'valid %%'
            OR  stones_dqr.comment LIKE '%% valid'
            OR  stones_dqr.comment LIKE '%% valid %%'
            OR	stones_dqr.comment LIKE 'validated'
            OR	stones_dqr.comment LIKE 'validated %%'
            OR  stones_dqr.comment LIKE '%% validated'
            OR  stones_dqr.comment LIKE '%% validated %%'
        )

                ''',
            parameters=(project_id, stones_field, pounds_field)
        )

    def get_report_line(self, row):
        error = self.get_error_message(row['stones'], row['pounds'], row['stones_validated'])

        if error:
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                error
            )

    def get_error_message(self, stones, pounds, stones_validated):
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

        if not 20.0 < calculated_kg < 200.0 and stones_validated == 0:
            return 'Invalid weight'

        return

    def is_na(self, value):
        return (value or '').strip().replace('/', '').lower() == 'na'


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
    md.element_label,
    CASE WHEN dqr.res_id IS NULL THEN 0 ELSE 1 END validated
FROM redcap_data e
JOIN redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = e.project_id
    AND dqs.record = e.record
    AND dqs.field_name = e.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE e.project_id = %s
    AND e.field_name IN ({})
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = e.project_id
            AND stat.record = e.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

                '''.format(', '.join(['\'{}\''.format(f) for f in fields])),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        if self.is_invalid(row['value'], row['validated']):
            return '- {}: {}\r\n'.format(
                self._redcap_instance()['link_generator'](
                    row['record'], row['project_id'], row['record']),
                row['element_label']
            )

    def is_invalid(self, value, validated):
        if (value or '').strip().replace('/', '').lower() in ('na', ''):
            return False
        if not value.replace('.', '', 1).isdigit():
            return True
        if not 17.0 <= float(value) <= 80.0 and validated == 0:
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
LEFT JOIN redcap_data_quality_status dqs
    ON dqs.project_id = rec.project_id
    AND dqs.record = rec.record
    AND dqs.field_name = rec.field_name
LEFT JOIN redcap_data_quality_resolutions dqr
    ON dqr.status_id = dqs.status_id
    AND (
            dqr.comment LIKE 'valid'
        OR  dqr.comment LIKE 'valid %%'
        OR  dqr.comment LIKE '%% valid'
        OR  dqr.comment LIKE '%% valid %%'
        OR	dqr.comment LIKE 'validated'
        OR	dqr.comment LIKE 'validated %%'
        OR  dqr.comment LIKE '%% validated'
        OR  dqr.comment LIKE '%% validated %%'
    )
WHERE [i2b2ClinDataIntegration].dbo.[GetAgeAtDate](
        CONVERT(DATE, dob.value),
        CONVERT(DATE, rec.value)) NOT BETWEEN %s AND %s
    AND dob.field_name = %s
    AND dob.project_id = %s
    AND dqr.res_id IS NULL
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = dob.project_id
            AND stat.record = dob.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

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
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = a.project_id
            AND stat.record = a.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
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

WITH meta (project_id_a, project_title_a, field_name_a, field_label_a, project_id_b, project_title_b, field_name_b, field_label_b) AS (
	SELECT
		a.project_id,
		a.app_title,
		a.field_name,
		a.element_label,
		b.project_id,
		b.app_title,
		b.field_name,
		b.element_label
	FROM (
		SELECT
			rm.project_id,
			rp.app_title,
			rm.field_name,
			rm.element_label
		FROM {0}.redcap_metadata rm
		JOIN {0}.redcap_projects rp
			ON rp.project_id = rm.project_id
		WHERE rm.project_id = %s
			AND rm.field_name = %s
	) a
	CROSS JOIN (
		SELECT
			rm.project_id,
			rp.app_title,
			rm.field_name,
			rm.element_label
		FROM {1}.redcap_metadata rm
		JOIN {1}.redcap_projects rp
			ON rp.project_id = rm.project_id
		WHERE rm.project_id = %s
			AND rm.field_name = %s
	) b
), a (record, value) AS (
	SELECT
		rd.record,
		rd.value
	FROM {0}.redcap_data rd
	JOIN meta
		ON meta.project_id_a = rd.project_id
		AND meta.field_name_a = rd.field_name
),  b (record, value) AS (
	SELECT
		rd.record,
		rd.value
	FROM {1}.redcap_data rd
	JOIN meta
		ON meta.project_id_b = rd.project_id
		AND meta.field_name_b = rd.field_name
), p (record) AS (
	SELECT DISTINCT a.record
	FROM meta
	JOIN {0}.redcap_data a
		ON a.project_id = meta.project_id_a
    JOIN {1}.redcap_data b
		ON b.project_id = meta.project_id_b
        AND b.record = a.record
), s (record) AS (
    SELECT record
    FROM {0}.redcap_data
    WHERE project_id IN (SELECT project_id_a FROM meta)
		AND field_name IN ('study_status_comp_yn', 'study_status')
        AND RTRIM(LTRIM(COALESCE(value, ''))) = '0'

    UNION

    SELECT record
    FROM {1}.redcap_data
    WHERE project_id IN (SELECT project_id_b FROM meta)
		AND field_name IN ('study_status_comp_yn', 'study_status')
        AND RTRIM(LTRIM(COALESCE(value, ''))) = '0'
)

SELECT
	p.record,
    meta.field_label_a [field_name_a],
    meta.field_label_b [field_name_b],
    meta.project_id_a [project_id_a],
    meta.project_id_b [project_id_b],
    meta.project_title_a [project_title_a],
    meta.project_title_b [project_title_b]
FROM p
CROSS JOIN meta
LEFT JOIN a ON a.record = p.record
LEFT JOIN b ON b.record = p.record
WHERE p.record NOT IN (
	SELECT record
	FROM s
) AND COALESCE(a.value, '') <> COALESCE(b.value, '')


                '''.format(
                redcap_instance_a()['staging_database'],
                redcap_instance_b()['staging_database'],
            ),
            parameters=(
                project_id_a,
                field_name_a,
                project_id_b,
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


class RedcapFieldsMustExistWhenOthersExist(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        indicator_fields,
        consequence_fields,
        error_message,
        recipients,
        schedule=None
    ):
        self._redcap_instance = redcap_instance
        self._error_message = error_message

        super().__init__(
            introduction=("The following participants have the following "
                          "invalid data in REDCap"),
            recipients=recipients,
            schedule=schedule,
            conn=redcap_instance()['connection'],
            sql='''

SELECT
    DISTINCT a.record,
    a.project_id
FROM    redcap_data a
WHERE a.project_id = %s
    AND EXISTS (
        SELECT 1
        FROM    redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ({0})
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b.value) = 0
    )
    AND NOT EXISTS (
        SELECT 1
        FROM    redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ({1})
            AND i2b2ClinDataIntegration.dbo.IsNullOrEmpty(b.value) = 0
    )
    AND NOT EXISTS (
        SELECT 1
        FROM redcap_data stat
        WHERE stat.project_id = a.project_id
            AND stat.record = a.record
            AND stat.field_name IN ('study_status_comp_yn', 'study_status')
            AND RTRIM(LTRIM(COALESCE(stat.value, ''))) = '0'
        )

                '''.format(
                ', '.join(['%s'] * len(indicator_fields)),
                ', '.join(['%s'] * len(consequence_fields))
            ),
            parameters=(
                tuple([project_id]) +
                tuple(indicator_fields) +
                tuple(consequence_fields)
            )
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            self._error_message
        )


