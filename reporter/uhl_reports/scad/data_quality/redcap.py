#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import RECIPIENT_SCAD_ADMIN
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapMissingDataWhen,
    RedcapInvalidDate,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidNhsNumber,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
)


REDCAP_CLINICAL_VISIT_PROJECT_ID = 28
REDCAP_CLINICAL_VISIT_V2_PROJECT_ID = 77
REDCAP_REGISTRY_PROJECT_ID = 31
REDCAP_INSTANCE = RedcapInstance.internal

# SCAD Clinical Visit


class ScadClinicalRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [
                'scad_local_id',
                'dob',
                'gender',
                'ethnicity',
                'referral_site',
                'int_date',
                'rec_type',
                'scadreg_id',
                'consent_version',
                'consent_date',
                'part_height',
                'part_weight',
                'part_bmi',
                'part_pulse1',
                'part_bp1_sys',
                'part_bp_dias',
                'study_status',
            ],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'part_bp1_sys',
            'part_bp_dias',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            ['part_pulse1'],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            ['part_height'],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            ['part_weight'],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            ['part_bmi'],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [RECIPIENT_SCAD_ADMIN],
        )


# SCAD Clinical Visit V2


class ScadClinicalV2RedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [
                'rec_type',
                'rec_method',
                'record_v1_0_yn',
                'consent_date',
                'consent_version',
                'scadreg_id',
                'scad_id',
                'dob',
                'gender',
                'ethnicity',
                'study_status',
            ],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapMissingData_NotPostal(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [
                'part_height',
                'part_weight',
                'part_bmi',
                'part_pulse1',
                'part_bp1_sys',
                'part_bp_dias',
            ],
            'where_bloods_taken',
            '2',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'part_bp1_sys',
            'part_bp_dias',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_MRI(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'mri_b_line_syst_bp',
            'mri_b_line_diast_bp',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_Adeno(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'adeno_stress_syst_bp',
            'adeno_stress_diast_bp',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_AorticFlow(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'syst_bp_aortic_flow',
            'diast_bp_at_aortic_flow',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_ResetPerfusion(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'syst_bp_rest_perf',
            'diast_bp_at_rest_perf',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_PsychologicalStress(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'sys_bp_b4_psych_stress',
            'dias_bp_b4_psych_stress',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_PsychologicalStressImages(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'psycho_stress_syst_bp',
            'psycho_stress_diast_bp',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBloodPressure_Baseline(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            'baseline_systolic_bp',
            'baseline_diastolic_bp',
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidHeartRate(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [
                'mri_b_line_hr',
                'adeno_stress_hr',
                'hr_at_aortic_flow',
                'hr_at_rest_perf',
                'hr_before_psych_stress',
                'psycho_stress_hr',
                'baseline_hr',
                'maximum_hr',
                'hrr_1_min',
                'hrr_2_min',
                'hrr_3_min',
                'part_pulse1',
            ],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [
                'part_height',
                'mri_height',
            ],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [
                'part_weight',
                'mri_weight',
            ],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            ['part_bmi'],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadClinicalV2RedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [RECIPIENT_SCAD_ADMIN],
        )


# SCAD Registry & Screening Visit


class ScadRegistryRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_REGISTRY_PROJECT_ID,
            [
                'reg_mode',
                'scad_reg_date',
                'scad_reg_typ',
                'frst_nm',
                'lst_nm',
                'gender',
                'dob',
                'addrss_pstcd',
                'consent_version',
                'nhs_no'
            ],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadRegistryInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_REGISTRY_PROJECT_ID,
            ['nhs_no'],
            [RECIPIENT_SCAD_ADMIN],
        )


class ScadRegistryInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_REGISTRY_PROJECT_ID,
            ['s_number'],
            [RECIPIENT_SCAD_ADMIN],
        )
