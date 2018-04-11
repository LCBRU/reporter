#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.reports.civicrm import get_contact_link
from reporter.reports.emailing import RECIPIENT_IT_DQ


class CivicrmPracticeDuplicateName(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following GP Practices have "
                          "a duplicate name in CiviCRM"),
            recipients=[RECIPIENT_IT_DQ],
            sql='''
                SELECT
                    con.id,
                    con.organization_name
                FROM (
                    SELECT
                        organization_name
                    FROM STG_CiviCRM.dbo.civicrm_contact con
                    WHERE con.contact_type = 'Organization'
                        AND con.contact_sub_type LIKE '%GP_Surgery%'
                        AND con.is_deleted = 0
                    GROUP BY con.organization_name
                    HAVING COUNT(*) > 1
                ) x
                JOIN STG_CiviCRM.dbo.civicrm_contact con
                    ON con.organization_name = x.organization_name
                    AND con.contact_sub_type LIKE '%GP_Surgery%'
                    AND con.is_deleted = 0
                ;
                ''',
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_contact_link(
                row['organization_name'], row['id']))
