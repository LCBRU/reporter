#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (get_case_link,
                      RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCS_ADMIN,
                      RECIPIENT_BRAVE_MANAGER, RECIPIENT_BRAVE_ADMIN,
                      RECIPIENT_GENVASC_MANAGER, RECIPIENT_GENVASC_ADMIN,
                      RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN,
                      RECIPIENT_BIORESOURCE_MANAGER,
                      RECIPIENT_BIORESOURCE_ADMIN,
                      RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN
                      )


class CivicrmInvalidCaseStatus(Report):
    def __init__(self, study_name, valid_statuses, recipients):
        super().__init__(
            name="CiviCRM Invalid Case Status ({})".format(study_name),
            introduction=("The following cases for the {} study have "
                          "invalid statuses:".format(study_name)),
            recipients=recipients,
            sql='''

SELECT
    cas.id AS case_id,
    con.id AS contact_id,
    cs.label AS case_status
FROM    STG_CiviCRM.dbo.civicrm_case cas
JOIN    STG_CiviCRM.dbo.civicrm_case_contact cas_con
    ON cas_con.case_id = cas.id
JOIN    STG_CiviCRM.dbo.civicrm_contact con
    ON con.id = cas_con.contact_id
    AND con.is_deleted = 0
JOIN    STG_CiviCRM.dbo.civicrm_case_type ct
    ON ct.id = cas.case_type_id
JOIN    STG_CiviCRM.dbo.civicrm_option_value cs
    ON cs.value = cas.status_id
    AND cs.option_group_id = 27
WHERE   cas.is_deleted = 0
    AND ct.name = %s
    AND cs.label NOT IN ({})
;

                '''.format(','.join(['%s'] * len(valid_statuses))),
                parameters=tuple([study_name]) + tuple(valid_statuses),
                schedule=Schedule.daily
        )

    def get_report_line(self, row):
        return '- {}\r\n'.format(
            get_case_link(
                row['case_status'],
                row['case_id'],
                row['contact_id']
            )
        )


class BioresourceCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'BIORESOURCE',
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_BIORESOURCE_MANAGER, RECIPIENT_BIORESOURCE_ADMIN])


class BioresourceSubStudyCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'BIORESOURCE_SUB_STUDY',
            [
                'Recruited',
                'Available for cohort',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Withdrawn'
            ],
            [RECIPIENT_BIORESOURCE_MANAGER, RECIPIENT_BIORESOURCE_ADMIN])


class BriccsCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'BRICCS',
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCS_ADMIN])


class BraveCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [
                'Recruited',
                'Completed',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_BRAVE_MANAGER, RECIPIENT_BRAVE_ADMIN])


class GenvascCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'GENVASC',
            [
                'Available for cohort',
                'Recruited',
                'Excluded',
                'Withdrawn'
            ],
            [RECIPIENT_GENVASC_MANAGER, RECIPIENT_GENVASC_ADMIN])


class ScadCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'SCAD',
            [
                'Recruited',
                'Completed',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN])


class TmaoCivicrmInvalidCaseStatus(CivicrmInvalidCaseStatus):
    def __init__(self):
        super().__init__(
            'TMAO',
            [
                'Recruited',
                'Declined',
                'Failed to Respond',
                'Recruitment Pending',
                'Excluded',
                'Duplicate',
                'Withdrawn'
            ],
            [RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN])
