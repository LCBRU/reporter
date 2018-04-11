#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.reports.civicrm import get_contact_link
from reporter.reports.emailing import RECIPIENT_IT_DQ


class CivicrmPracticeDuplicateCode(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following GP Practices do not have "
                          "a duplicate code in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''
        SELECT
            x.practice_code,
            con.id,
            con.display_name
        FROM (
            SELECT
                RTRIM(LTRIM(COALESCE(gp.practice_code_7, ''))) [practice_code]
            FROM STG_CiviCRM.dbo.civicrm_contact con
            LEFT JOIN STG_CiviCRM.dbo.civicrm_value_gp_surgery_data_3 gp
                ON gp.entity_id = con.id
            WHERE con.contact_type = 'Organization'
                AND con.contact_sub_type LIKE '%GP_Surgery%'
                AND con.is_deleted = 0
                AND LEN(RTRIM(LTRIM(COALESCE(gp.practice_code_7, '')))) > 0
            GROUP BY RTRIM(LTRIM(COALESCE(gp.practice_code_7, '')))
            HAVING COUNT(*) > 1
        ) x
        JOIN STG_CiviCRM.dbo.civicrm_value_gp_surgery_data_3 gp
            ON gp.practice_code_7 = x.practice_code
        JOIN STG_CiviCRM.dbo.civicrm_contact con
            ON con.id = gp.entity_id
            AND con.is_deleted = 0
        ;
                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            row['practice_code'],
            get_contact_link(
                row['display_name'], row['id']))
