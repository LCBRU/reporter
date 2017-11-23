#!/usr/bin/env python3

from reporter.reports import Report
from reporter import (
    RedcapInstance,
    RECIPIENT_FAST_ADMIN
)
from reporter.reports.redcap.missing_data import (
    RedcapInvalidStudyNumber,
    RedcapInvalidDate,
    RedcapInvalidNhsNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidHeightInFeetAndInches,
    RedcapInvalidWeightInKg,
    RedcapInvalidWeightInStonesAndPounds,
    RedcapInvalidBmi,
    RedcapImpliesCheck
)


class FastRedcapMissingData(Report):
    def __init__(self):
        self._redcap_instance = RedcapInstance.internal
        project_id = 43
        fields = ['nhs_number', 'gender', 'ethnicity', 'dob',
                  'date', 'practice_location', 'invitation_grp',
                  'invitation_type', 'iti_max_ap', 'iti_max_trnsvrs',
                  'sys_bp', 'dias_bp', 'pulse']
        recipients = [RECIPIENT_FAST_ADMIN]
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
    JOIN STG_redcap.dbo.redcap_metadata md
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
AND EXISTS (
    SELECT 1
    FROM    [i2b2_app03_fast_Data].[dbo].[LOAD_FullyConsented] fc
    WHERE fc.StudyNumber = pe.record
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


class FastRedcapInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['nhs_number'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['fst_label', 'record_id'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            'sys_bp',
            'dias_bp',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['pulse'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['height_cms'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidHeightInFeetAndInches(
        RedcapInvalidHeightInFeetAndInches):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            'height_ft',
            'height_inches',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['weight_kgs'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidWeightInStonesAndPounds(
        RedcapInvalidWeightInStonesAndPounds):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            'weight_stones',
            'weight_pounds',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['bmi'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['dob', 'date'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastCurrentSmokerGroupButNotCurrentSmoker(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['0'],
            ['curr_smoke'],
            ['1'],
            'Participant in current smoker group, but is not a current smoker',
            [RECIPIENT_FAST_ADMIN]
        )


class FastExSmokerGroupButNotExSmoker(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['1'],
            ['ex_smoker'],
            ['1'],
            'Participant in Ex-smoker group, but is not an ex-smoker',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRiskFactorGroupButNoRiskFactors(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['2'],
            ['diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol', 'fam_hist_aaa',
             'reg_meds'],
            ['1', '2', '3', '4'],
            'Participant in risk factor group, but is has no risk factors',
            [RECIPIENT_FAST_ADMIN]
        )


class FastNoRiskFactorGroupButHasRiskFactors(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['3'],
            ['diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol',
             'reg_meds', 'curr_smoke', 'ex_smoker'],
            ['1', '2', '3', '4'],
            'Participant in no risk factors group, but is has risk factors',
            [RECIPIENT_FAST_ADMIN],
            True
        )


class FastEthnicMinorityGroupButNotInEthnicMinority(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['4'],
            ['ethnicity'],
            ['D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'],
            'Participant in ethinic minority group, '
            'but is not in an ethnic minority',
            [RECIPIENT_FAST_ADMIN]
        )


class FastSiblingsGroupButNoFamilyHistory(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['5'],
            ['fam_hist_aaa'],
            ['1'],
            'Participant in siblings group, but has no family history of AAA',
            [RECIPIENT_FAST_ADMIN]
        )


class FastWhiteEthnicGroupButInEthinicMinority(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['0', '1', '2', '3'],
            ['ethnicity'],
            ['D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'],
            'Participant in white ethnic group, but in ethnic minority',
            [RECIPIENT_FAST_ADMIN],
            True
        )
