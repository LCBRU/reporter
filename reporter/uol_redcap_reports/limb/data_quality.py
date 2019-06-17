#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_LIMB_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_LIMB_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidHeightInM,
    RedcapInvalidWeightInKg,
    RedcapInvalidPulse,
    RedcapInvalidBmi,
    RedcapInvalidBloodPressure,
)

REDCAP_PROJECT_ID = 32


class LimbRedcapStudyNumber(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^[A-Z]{2}\d{4}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['weight_kg', 'pre_interv_weight', 'post_interv_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidHeightInM(RedcapInvalidHeightInM):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['height_m', 'pre_interv_height', 'post_interv_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBmi(RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['pre_interv_bmi', 'post_interv_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidPulse(RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=[
                'hr_bpm',
                'pre_interv_mri_rest_hr',
                'pre_interv_mri_stress_hr',
                'post_interv_mri_rest_hr',
                'post_interv_mri_stress_hr',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_Baseline(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='sbp_mmhg',
            diastolic_field_name='dbp_mmhg',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_MriRest(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='pre_interv_mri_rest_sbp',
            diastolic_field_name='pre_interv_mri_rest_dbp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_MriStress(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='pre_interv_mri_stress_sbp',
            diastolic_field_name='pre_interv_mri_stress_dbp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_AoCine(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='pre_interv_mri_syst_bp_ao_cine',
            diastolic_field_name='pre_interv_mri_diast_bp_ao_cine',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_PostMriRest(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='post_interv_mri_rest_sbp',
            diastolic_field_name='post_interv_mri_rest_dbp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_PostMriStress(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='post_interv_mri_stress_sbp',
            diastolic_field_name='post_interv_mri_stress_dbp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbRedcapInvalidBloodPressure_PostAoCine(RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            systolic_field_name='post_interv_mri_syst_bp_ao_cine',
            diastolic_field_name='post_interv_mri_diast_bp_ao_cine',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


