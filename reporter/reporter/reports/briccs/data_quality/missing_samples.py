#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.emailing import RECIPIENT_BRICCS_ADMIN

# Abstract Classes


class BriccsRedcapBloodSamplesMissing(Report):
    def __init__(self, database, schedule=None):
        super().__init__(
            introduction=("The following participants have "
                          "should have blood samples in REDCap, "
                          "but do not"),
            recipients=[RECIPIENT_BRICCS_ADMIN],
            schedule=schedule or Schedule.weekly,

            sql='''

SELECT
    bt.record [StudyNumber],
    p.project_name
FROM    {0}.dbo.redcap_data bt
JOIN    {0}.dbo.redcap_projects p
    ON p.project_id = bt.project_id
LEFT JOIN   STG_redcap.dbo.redcap_data b1
    ON b1.record = bt.record
    AND b1.project_id = bt.project_id
    AND b1.field_name = 'blood_tube1'
    AND LEN(RTRIM(LTRIM(COALESCE(b1.value, '')))) > 0
LEFT JOIN   {0}.dbo.redcap_data b2
    ON b2.record = bt.record
    AND b2.project_id = bt.project_id
    AND b2.field_name = 'blood_tube2'
    AND LEN(RTRIM(LTRIM(COALESCE(b2.value, '')))) > 0
LEFT JOIN   {0}.dbo.redcap_data b3
    ON b3.record = bt.record
    AND b3.project_id = bt.project_id
    AND b3.field_name = 'blood_tube3'
    AND LEN(RTRIM(LTRIM(COALESCE(b3.value, '')))) > 0
LEFT JOIN   {0}.dbo.redcap_data b4
    ON b4.record = bt.record
    AND b4.project_id = bt.project_id
    AND b4.field_name = 'blood_tube4'
    AND LEN(RTRIM(LTRIM(COALESCE(b4.value, '')))) > 0
LEFT JOIN   {0}.dbo.redcap_data b5
    ON b5.record = bt.record
    AND b5.project_id = bt.project_id
    AND b5.field_name = 'blood_tube5'
    AND LEN(RTRIM(LTRIM(COALESCE(b5.value, '')))) > 0
WHERE bt.project_id = 24
    AND bt.field_name = 'blood_taken'
    AND bt.value = 1
    AND COALESCE(b1.value, b2.value, b3.value, b4.value, b5.value) IS NULL

                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {} ({})\r\n'.format(
            row['StudyNumber'],
            row['project_name'])


class BriccsRedcapUrineSamplesMissing(Report):
    def __init__(self, database, schedule=None):
        super().__init__(
            introduction=("The following participants have "
                          "should have urine samples in REDCap, "
                          "but do not"),
            recipients=[RECIPIENT_BRICCS_ADMIN],
            schedule=schedule or Schedule.weekly,

            sql='''

SELECT
    bt.record [StudyNumber],
    p.project_name
FROM    {0}.dbo.redcap_data bt
JOIN    {0}.dbo.redcap_projects p
    ON p.project_id = bt.project_id
LEFT JOIN   {0}.dbo.redcap_data u
    ON u.record = bt.record
    AND u.project_id = bt.project_id
    AND u.field_name = 'urine_sample'
    AND LEN(RTRIM(LTRIM(COALESCE(u.value, '')))) > 0
WHERE bt.project_id = 24
    AND bt.field_name = 'taken_urine_sample'
    AND bt.value = 1
    AND u.value IS NULL

                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {} ({})\r\n'.format(
            row['StudyNumber'],
            row['project_name'])

# Glenfield


class GlenfieldBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__('STG_redcap')


class GlenfieldBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__('STG_redcap')


# External


class ExternalBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__('STG_redcap_briccsext')


class ExternalBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__('STG_redcap_briccsext')
