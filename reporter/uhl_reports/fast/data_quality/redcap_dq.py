#!/usr/bin/env python3

from reporter.core import SqlReport, Schedule
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_FAST_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_FAST_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.application_abstract_reports.redcap.data_quality import (
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
    RedcapImpliesCheck,
    RedcapOutsideAgeRange,
    RedcapMissingData,
    RedcapMissingDataWhen,
    RedcapMissingDataWhenNot,
)
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_CRF_PROJECT_ID = 43
REDCAP_SCREENING_PROJECT_ID = 48
REDCAP_INSTANCE = RedcapInstance.internal


class FastClinicalRedcapMissingData(SqlReport):
    def __init__(self):
        fields = [
            'nhs_number',
            'gender',
            'ethnicity',
            'dob',
            'date',
            'practice_location',
            'invitation_grp',
            'invitation_type',
            'iti_max_ap',
            'iti_max_trnsvrs',
        ]
        recipients = [RECIPIENT_ADMIN]
        schedule = None

        super().__init__(
            introduction=("The following participants have data "
                          "missing from REDCap"),
            recipients=recipients,
            schedule=schedule,
            conn=REDCAP_INSTANCE()['connection'],
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN redcap_metadata md
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
    FROM redcap_data e
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
                    ', '.join(['\'{}\''.format(f) for f in fields])
                ),
            parameters=(REDCAP_CRF_PROJECT_ID)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            REDCAP_INSTANCE()['link_generator'](
                row['record'],
                row['project_id'],
                row['record'],
            ),
            row['error_message']
        )


class FastClinicalRedcapMissingMeasurements(SqlReport):
    def __init__(self):
        fields = [
            'sys_bp',
            'dias_bp',
            'pulse'
        ]
        recipients = [RECIPIENT_ADMIN]
        schedule = None

        super().__init__(
            introduction=("The following participants have measurements "
                          "missing from REDCap"),
            recipients=recipients,
            schedule=schedule,
            conn=REDCAP_INSTANCE()['connection'],
            sql='''

WITH recruited AS (
    SELECT  DISTINCT record, project_id
    FROM    redcap_data
    WHERE project_id = %s
), potential_errors AS (
    SELECT
        r.record,
        r.project_id,
        md.field_name,
        'Missing ' + REPLACE(md.element_label, '\r\n', ' ') [error]
    FROM recruited r
    JOIN redcap_metadata md
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
    FROM redcap_data e
    WHERE e.project_id = pe.project_id
        AND e.record = pe.record
        AND e.field_name = pe.field_name
        AND LEN(RTRIM(LTRIM(COALESCE(e.value, '')))) > 0
)
AND NOT EXISTS (
    SELECT 1
    FROM    [i2b2_app03_fast_Data].[dbo].[LOAD_FullyConsented] fc
    WHERE fc.StudyNumber = pe.record
)
AND NOT EXISTS (
    SELECT 1
    FROM redcap_data dt
	WHERE dt.project_id = pe.project_id
        AND dt.record = pe.record
		AND dt.field_name = 'date'
		AND dt.value >= '2018-02-05'
)
ORDER BY pe.record

                '''.format(
                    ', '.join(['\'{}\''.format(f) for f in fields])
                ),
            parameters=(REDCAP_CRF_PROJECT_ID)
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            REDCAP_INSTANCE()['link_generator'](
                row['record'],
                row['project_id'],
                row['record'],
            ),
            row['error_message']
        )


class FastClinicalRedcapInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=['fst_label', 'record_id'],
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            systolic_field_name='sys_bp',
            diastolic_field_name='dias_bp',
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=['pulse'],
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=['height_cms'],
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidHeightInFeetAndInches(
        RedcapInvalidHeightInFeetAndInches):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            feet_field='height_ft',
            inches_field='height_inches',
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=['weight_kgs'],
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidWeightInStonesAndPounds(
        RedcapInvalidWeightInStonesAndPounds):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            stones_field='weight_stones',
            pounds_field='weight_pounds',
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=['bmi'],
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN],
        )

class FastCurrentSmokerGroupButNotCurrentSmoker(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['0'],
            consequence_fields=['curr_smoke'],
            consequence_values=['1'],
            error_message='Participant in current smoker group, but is not a current smoker',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastExSmokerGroupButNotExSmoker(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['1'],
            consequence_fields=['ex_smoker'],
            consequence_values=['1'],
            error_message='Participant in Ex-smoker group, but is not an ex-smoker',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastRiskFactorGroupButNoRiskFactors(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['2'],
            consequence_fields=['diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol', 'fam_hist_aaa',
             'reg_meds'],
            consequence_values=['1', '2', '3', '4'],
            error_message='Participant in risk factor group, but is has no risk factors',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastNoRiskFactorGroupButHasRiskFactors(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['3'],
            consequence_fields=['diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol',
             'reg_meds', 'curr_smoke', 'ex_smoker'],
            consequence_values=['1', '2', '3', '4'],
            error_message='Participant in no risk factors group, but is has risk factors',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
            reverse=True,
        )


class FastEthnicMinorityGroupButNotInEthnicMinority(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['4'],
            consequence_fields=['ethnicity'],
            consequence_values=['D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'],
            error_message='Participant in ethinic minority group, '
            'but is not in an ethnic minority',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastSiblingsGroupButNoFamilyHistory(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['5'],
            consequence_fields=['fam_hist_aaa'],
            consequence_values=['1'],
            error_message='Participant in siblings group, but has no family history of AAA',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class FastWhiteEthnicGroupButInEthinicMinority(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            indicator_fields=['invitation_grp'],
            indicator_values=['0', '1', '2', '3'],
            consequence_fields=['ethnicity'],
            consequence_values=['D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'],
            error_message='Participant in white ethnic group, but in ethnic minority',
            recipients=[RECIPIENT_ADMIN],
            schedule=Schedule.never,
            reverse=True,
        )


class FastRedcapOutsideAgeRange(
        RedcapOutsideAgeRange):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            dob_field='dob',
            recruited_date_field='date',
            min_age=65,
            max_age=75,
            recipients=[RECIPIENT_ADMIN],
        )


class FastRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'FAST',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class FastRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='FAST',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


class FastRedcapCrfWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ],
        )


class FastRedcapScreeningWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ],
        )


class FastRedcapMissingConsent(RedcapMissingData):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=[
                'res_consent_2',
                'res_consent_3',
                'res_consent_4',
                'res_consent_5',
                'res_consent_6',
                'res_consent_7',
                'opt_consent_8',
                'opt_consent_9',
                'opt_consent_11',
                'opt_consent_12',
                'opt_consent_13',
                'opt_consent_14',
                'consent_ext_dta_coll',
                'consent_hscic',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class FastRedcapMissingConsentEDQ5(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_CRF_PROJECT_ID,
            fields=[
                'opt_consent_10',
            ],
            indicator_field='date',
            indicator_value='2018-01-29',
            comparator='<',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class FastRedcapMissingPisConsent(RedcapMissingDataWhenNot):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=[
                'res_consent_1a',
            ],
            indicator_field='invitation_grp',
            indicator_value='5',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class FastRedcapMissingSiblingPisConsent(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=[
                'res_consent_1',
            ],
            indicator_field='invitation_grp',
            indicator_value='5',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
