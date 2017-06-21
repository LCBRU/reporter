#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import get_contact_link, RECIPIENT_IT_DQ


class CivicrmPracticeMissingCode(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following GP Practices do not have "
                          "codes in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''
                SELECT
                    con.display_name,
                    con.id
                FROM STG_CiviCRM.dbo.civicrm_contact con
                LEFT JOIN STG_CiviCRM.dbo.civicrm_value_gp_surgery_data_3 gp
                    ON gp.entity_id = con.id
                WHERE con.contact_type = 'Organization'
                    AND con.contact_sub_type LIKE '%GP_Surgery%'
                    AND con.is_deleted = 0
                    AND LEN(RTRIM(LTRIM(COALESCE(gp.practice_code_7, '')))) = 0
                ;
                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(
                row['display_name'], row['id']))
