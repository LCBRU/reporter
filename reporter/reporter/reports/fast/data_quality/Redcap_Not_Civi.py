#!/usr/bin/env python3

from reporter.reports import SqlReport, Schedule
from reporter.reports.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)
from reporter.reports.redcap import get_redcap_link


class FastRedcapNotCivicrmReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants are "
                          "recruited in REDCap, but are not "
                          "recruited is CiviCRM:"),
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
            schedule=Schedule.weekly,
            sql='''
SELECT
    ri.value AS fast_id,
    ri.project_id AS project_id,
    ri.record
FROM    STG_redcap.dbo.redcap_data ri
JOIN    STG_redcap.dbo.redcap_data pr
    ON pr.record = ri.record
    AND pr.project_id = ri.project_id
    AND pr.field_name = 'patient_reruited'
WHERE   ri.project_id = 48
    AND ri.field_name = 'record_id'
    AND pr.value = '1'
    AND NOT EXISTS (
        SELECT  1
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
            AND fst.fast_id_106 = ri.value
    )

                '''
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_redcap_link(
                row['fast_id'],
                row["project_id"],
                row["record"]))
