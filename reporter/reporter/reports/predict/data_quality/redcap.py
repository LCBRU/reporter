#!/usr/bin/env python3

from reporter.reports import Report
from reporter.reports.databases import RedcapInstance
from reporter.reports.emailing import RECIPIENT_PREDICT_ADMIN
from reporter.reports.redcap.data_quality import (
    RedcapInvalidStudyNumber,
    RedcapInvalidNhsNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi
)


class PredictRedcapMissingData(Report):
    def __init__(self):
        self._redcap_instance = RedcapInstance.internal
        project_id = 62
        fields = ['nhs_number', 'gender', 'ethnicity', 'dob',
                  'date', 'practice_location', 'invitation_grp',
                  'invitation_type', 'iti_max_ap', 'iti_max_trnsvrs',
                  'sys_bp', 'dias_bp', 'pulse']
        recipients = [RECIPIENT_PREDICT_ADMIN]
        schedule = None

        super().__init__(
            introduction=("The following participants have data "
                          "missing from REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    {1}.dbo.redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN {1}.dbo.redcap_metadata md
        ON md.project_id = r.project_id
        AND md.field_name IN ({0})
)
SELECT
    pe.project_id,
    pe.record,
    pe.error AS [error_message]
FROM potential_errors pe
WHERE NOT EXISTS (
    SELECT 1
    FROM {1}.dbo.redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
ORDER BY pe.record

                '''.format(
                ', '.join(['\'{}\''.format(f) for f in fields]),
                self._redcap_instance()['staging_database']),
            parameters=(project_id)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['error_message']
        )


class PredictRedcapInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            ['nhs_number'],
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            ['record_id'],
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            'sbp1_mmhg',
            'dbp1_mmhg',
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            'sbp2_mmhg',
            'dbp2_mmhg',
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            'sbp3_mmhg',
            'dbp3_mmhg',
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            'avg_sbp_mmhg',
            'avg_dbp_mmhg',
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            ['hr1_bpm', 'hr2_bpm', 'hr3_bpm', 'avg_hr_bpm'],
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            ['height_cm'],
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            ['weight_kg'],
            [RECIPIENT_PREDICT_ADMIN]
        )


class PredictRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            62,
            ['bmi_kg_m2'],
            [RECIPIENT_PREDICT_ADMIN]
        )

'''
r = PredictRedcapInvalidBmi()
r.run()
r = PredictRedcapInvalidPulse()
r.run()
r = PredictRedcapMissingData()
r.run()
r = PredictRedcapInvalidBloodPressure1()
r.run()
r = PredictRedcapInvalidBloodPressure2()
r.run()
r = PredictRedcapInvalidBloodPressure3()
r.run()
r = PredictRedcapInvalidNhsNumber()
r.run()
r = PredictRedcapInvalidStudyNumber()
r.run()
r = PredictRedcapInvalidBloodPressureAvg()
r.run()
r = PredictRedcapInvalidHeightInCm()
r.run()
r = PredictRedcapInvalidWeightInKg()
r.run()
r = PredictRedcapRecordInvalidStudyNumber()
r.run()
'''