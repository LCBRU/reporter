#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN
)
from reporter.reports.civicrm import get_case_link


class FastCivicrmNotRedcapReport(Report):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants are "
                          "recruited in civicrm, but are not "
                          "recruited is REDCap:"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''
SELECT
    con.id AS civicrm_contact_id,
    cas.id AS civicrm_case_id,
    fst.fast_id_106 AS fast_id
FROM    STG_CiviCRM.dbo.civicrm_case cas
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
JOIN    STG_CiviCRM.dbo.civicrm_value_fast_24 fst
    ON fst.entity_id = cas.id
WHERE cas.case_type_id = 18 -- FAST
    AND cas.is_deleted = 0
    AND cas.status_id = 5 -- Recruited
    AND NOT EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data ri
        JOIN    STG_redcap.dbo.redcap_data pr
            ON pr.record = ri.record
            AND pr.project_id = ri.project_id
            AND pr.field_name = 'patient_reruited'
        WHERE   ri.project_id = 48
            AND ri.field_name = 'record_id'
            AND pr.value = '1'
            AND ri.value = fst.fast_id_106
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['fast_id'] or 'Click Here',
                row["civicrm_case_id"],
                row["civicrm_contact_id"]))
