#!/usr/bin/env python3

import pandas as pd
import datetime
from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_FAST_MANAGER as RECIPIENT_MANAGER,
)
from reporter.connections import RedcapInstance


class FastGroupErrors(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following Glenfield participants are "
                          "in Onyx, but are not in CiviCrm"),
            recipients=[RECIPIENT_MANAGER],
            sql='''


SELECT
	'Participant in current smoker group, but is not a current smoker' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('0')
    AND NOT EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('curr_smoke')
            AND b.value IN ('1')
    )
UNION
SELECT
	'Participant in Ex-smoker group, but is not an ex-smoker' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('1')
    AND NOT EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('ex_smoker')
            AND b.value IN ('1')
    )
UNION
SELECT
	'Participant in risk factor group, but has no risk factors' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('2')
    AND NOT EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol', 'fam_hist_aaa',
             'reg_meds')
            AND b.value IN ('1', '2', '3', '4')
    )
UNION
SELECT
	'Participant in no risk factors group, but has risk factors' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('3')
    AND EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol',
             'reg_meds', 'curr_smoke', 'ex_smoker')
            AND b.value IN ('1', '2', '3', '4')
    )
UNION
SELECT
	'Participant in ethinic minority group, but is not in an ethnic minority' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('4')
    AND NOT EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('ethnicity')
            AND b.value IN ('D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S')
    )
UNION
SELECT
	'Participant in siblings group, but has no family history of AAA' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('5')
    AND NOT EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('fam_hist_aaa')
            AND b.value IN ('1')
    )
UNION
SELECT
	'Participant in white ethnic group, but in ethnic minority' [error],
	COUNT(*) [count]
FROM    STG_redcap.dbo.redcap_data a
WHERE a.project_id = 43
    AND a.field_name IN ('invitation_grp')
    AND a.value IN ('0', '1', '2', '3')
    AND EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ('ethnicity')
            AND b.value IN ('D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S')
    )


                '''
        )

    def get_report(self):
        markdown = ''

        markdown += '# FAST Errors in Groups {0:%d-%b-%Y}\r\n\r\n'.format(datetime.datetime.now())

        columns = [
            'Error',
            'Count',
        ]

        markdown += ' | '.join(columns) + '\r\n'
        markdown += ' | '.join(['-' * len(x) for x in columns]) + '\r\n'

        with self._conn() as cursor:

            df = pd.io.sql.read_sql(
                self._sql,
                cursor.connection)

            for _, row in df.iterrows():
                markdown += ' | '.join([str(v) for v in [
                    row['error'],
                    row['count'],
                ]]) + '\r\n'

            return markdown, 1, []
