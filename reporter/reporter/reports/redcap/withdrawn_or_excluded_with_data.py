#!/usr/bin/env python3

from itertools import groupby
from reporter.reports import Report, Schedule
from reporter import (
    RECIPIENT_BIORESOURCE_MANAGER, RECIPIENT_BIORESOURCE_ADMIN,
    RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCS_ADMIN,
    RECIPIENT_BRAVE_MANAGER, RECIPIENT_BRAVE_ADMIN,
    RECIPIENT_DREAM_MANAGER, RECIPIENT_DREAM_ADMIN,
    RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN,
    RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN,
    RECIPIENT_GRAPHIC2_MANAGER)


class RedcapWithdrawnOrExcludedWithDataReport(Report):
    def __init__(self, study_name, recipients):
        super().__init__(
            name="Withdrawn or Excluded with Data Report ({})".format(
                study_name),
            introduction=("Withdrawn or excluded participants with date"
                          "in REDCap for {} study".format(study_name)),
            recipients=recipients,
            schedule=Schedule.weekly,
            sql='''

SELECT
    p.app_title AS [Questionnaire],
    csn.StudyNumber
FROM    STG_CiviCRM.dbo.civicrm_case cas
JOIN    STG_CiviCRM.dbo.civicrm_case_type ct
    ON ct.id = cas.case_type_id
JOIN    STG_CiviCRM.dbo.CaseStudyNumber csn
    ON csn.case_id  = cas.id
JOIN (
    SELECT 8 [project_id], 4 [case_type_id] UNION -- Dream
    SELECT 9 [project_id], 7 [case_type_id] UNION -- Bioresource
    SELECT 20 [project_id], 5 [case_type_id] UNION -- GRAPHIC 2
    SELECT 22 [project_id], 4 [case_type_id] UNION -- Dream
    SELECT 24 [project_id], 6 [case_type_id] UNION -- BRICCS
    SELECT 25 [project_id], 12 [case_type_id] UNION -- TMAO
    SELECT 26 [project_id], 10 [case_type_id] UNION -- BRAVE
    SELECT 28 [project_id], 9 [case_type_id] UNION -- SCAD
    SELECT 29 [project_id], 10 [case_type_id] UNION -- BRAVE
    SELECT 37 [project_id], 6 [case_type_id] UNION -- BRICCS AS
    SELECT 55 [project_id], 7 [case_type_id] -- INTERVAL - Hence Bioresource
) rpr ON rpr.case_type_id = cas.case_type_id
JOIN    STG_redcap.dbo.redcap_projects p
    ON p.project_id = rpr.project_id
WHERE cas.is_deleted = 0
    AND ct.name = %s
    AND cas.status_id IN (
        8, -- Withdrawn
        9 -- Excluded
    ) AND EXISTS (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data rd
        JOIN    STG_redcap.dbo.redcap_metadata meta
            ON meta.project_id = rd.project_id
                AND meta.field_name = rd.field_name
                AND meta.form_name NOT IN (
                    'screening',
                    'consent'
                )
        WHERE   rd.project_id = rpr.project_id
            AND rd.record = csn.StudyNumber
    )
ORDER BY Questionnaire, StudyNumber

                ''',
            parameters=(study_name),
        )

    def get_report_lines(self, cursor):
        markdown = ''

        for questionnaire, participants in groupby(cursor, lambda x: x['Questionnaire']):
            markdown += "**{}**\r\n\r\n".format(questionnaire)

            for p in participants:
                markdown += "- {}\r\n".format(p['StudyNumber'])

            markdown += "\r\n\r\n".format()

        return markdown, cursor.rowcount + 1


class BioresourceRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Bioresource',
            [RECIPIENT_BIORESOURCE_MANAGER, RECIPIENT_BIORESOURCE_ADMIN])


class BraveRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [RECIPIENT_BRAVE_ADMIN, RECIPIENT_BRAVE_MANAGER])


class BriccsRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'BRICCS',
            [RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCS_ADMIN])


class DreamRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'DREAM',
            [RECIPIENT_DREAM_MANAGER, RECIPIENT_DREAM_ADMIN])


class Graphic2RedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Graphic2',
            [RECIPIENT_GRAPHIC2_MANAGER])


class ScadRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'SCAD',
            [RECIPIENT_SCAD_MANAGER, RECIPIENT_SCAD_ADMIN])


class TmaoRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'TMAO',
            [RECIPIENT_TMAO_MANAGER, RECIPIENT_TMAO_ADMIN])
