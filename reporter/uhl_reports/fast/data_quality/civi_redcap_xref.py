#!/usr/bin/env python3

from reporter.uhl_reports.civicrm.civicrm_redcap_xref import (
    CivicrmNotInRedcap,
)
from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_IT_DWH,
)
from reporter.connections import get_redcap_link


CASE_TYPE_ID = 18
FAST_SCREENING_REDCAP_PROJECT_ID = 48
FAST_CLINICAL_REDCAP_PROJECT_ID = 43


class FastScreeningCivicrmNotInRedcap(CivicrmNotInRedcap):
    def __init__(self):
        super().__init__(
            case_type_ids=[CASE_TYPE_ID],
            redcap_project_ids=[FAST_SCREENING_REDCAP_PROJECT_ID],
        )


class FastRedcapNotCivicrmReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following FAST participants are "
                          "recruited in REDCap, but are not "
                          "recruited is CiviCRM:"),
            recipients=[RECIPIENT_IT_DWH],
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
    AND pr.field_name = 'patient_recruited'
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
            AND cas.status_id IN (
                5, -- Recruited
                8, -- Withdrawn
                9, -- Excluded
                10, -- Completed
                14 -- Duplicate
            )
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
