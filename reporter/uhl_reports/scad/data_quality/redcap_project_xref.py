#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.connections import RedcapInstance
from reporter.emailing import RECIPIENT_SCAD_ADMIN
from reporter.connections import get_redcap_link
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapXrefMismatch,
)


REDCAP_CLINICAL_VISIT_PROJECT_ID = 28
REDCAP_CLINICAL_VISIT_V2_PROJECT_ID = 77
REDCAP_REGISTRY_PROJECT_ID = 31


class ScadRegistryClinicMismatchReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The following SCAD participants have "
                          "a mismatch between the clinic and "
                          "registry data in REDCap:"),
            recipients=[RECIPIENT_SCAD_ADMIN],
            schedule=Schedule.weekly,
            sql='''

WITH clinic AS (
    SELECT
        record,
        value scadreg_id,
        project_id
    FROM    STG_redcap.dbo.redcap_data
    WHERE project_id = 28
        AND field_name = 'scadreg_id'
), reg AS (
    SELECT DISTINCT
        record,
        project_id
    FROM    STG_redcap.dbo.redcap_data
    WHERE project_id = 31
)
SELECT
    c.record [scad_id],
    c.project_id [scad_clinic_project_id],
    r.record [scadreg_id],
    r.project_id [scad_reg_project_id],
    'Registration types do not match' AS [error_message]
FROM    clinic c
JOIN    reg r
    ON r.record = c.scadreg_id
JOIN    STG_redcap.dbo.redcap_data cd
    ON cd.project_id = c.project_id
    AND cd.record = c.record
    AND cd.field_name = 'rec_type'
JOIN    STG_redcap.dbo.redcap_data rd
    ON rd.record = r.record
    AND rd.project_id = r.project_id
    AND rd.field_name = 'scad_reg_typ'
WHERE
    CASE cd.value
        WHEN 0 THEN 2
        WHEN 1 THEN 0
    END <> rd.value

                '''
        )

    def get_report_line(self, row):
        return '- {}: {} / {} - {}\r\n\r\n'.format(
            row['scad_id'],
            get_redcap_link(
                'Clinic',
                row['scad_clinic_project_id'],
                row['scad_id']
            ),
            get_redcap_link(
                'Registry',
                row['scad_reg_project_id'],
                row['scadreg_id']
            ),
            row['error_message']
        )


class ScadClinicVisitMismatchReport_dob(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=REDCAP_CLINICAL_VISIT_PROJECT_ID,
            field_name_a='dob',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=REDCAP_CLINICAL_VISIT_V2_PROJECT_ID,
            field_name_b='dob',
            recipients=[RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicVisitMismatchReport_gender(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=REDCAP_CLINICAL_VISIT_PROJECT_ID,
            field_name_a='gender',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=REDCAP_CLINICAL_VISIT_V2_PROJECT_ID,
            field_name_b='gender',
            recipients=[RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicVisitMismatchReport_ethnicity(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=REDCAP_CLINICAL_VISIT_PROJECT_ID,
            field_name_a='ethnicity',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=REDCAP_CLINICAL_VISIT_V2_PROJECT_ID,
            field_name_b='ethnicity',
            recipients=[RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicVisitMismatchReport_ScadRegId(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=REDCAP_CLINICAL_VISIT_PROJECT_ID,
            field_name_a='scadreg_id',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=REDCAP_CLINICAL_VISIT_V2_PROJECT_ID,
            field_name_b='scadreg_id',
            recipients=[RECIPIENT_SCAD_ADMIN]
        )
