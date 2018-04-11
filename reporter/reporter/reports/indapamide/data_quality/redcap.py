#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_INDAPAMIDE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_INDAPAMIDE_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapInvalidStudyNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidDate,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

CRF_PROJECT_ID = 50
SCREENING_PROJECT_ID = 54
REDCAP_INSTANCE = RedcapInstance.internal


class IndapamideRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Indapamide',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class IndapamideRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Indapamide',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class IndapamideRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [
                'record_id',
                'screening_date',
                'status',
                'dob',
                's_number',
                'gender',
                'ethnicity',
                'tobacco_any',
                'alcohol_ever',
                'part_hist_highbp',
                'part_hist_diab',
                'part_hist_chol',
                'part_hist_heart_failure',
                'part_hist_mi',
                'part_hist_cva',
                'part_hist_tia',
                'part_hist_angina',
                'part_hist_pvd',
                'part_hist_vhd',
                'part_hist_oth_cong_prob',
                'part_hist_aa',
                'part_hist_crf',
                'part_hist_copd',
                'part_hist_renal',
                'part_hist_asthm',
                'part_hist_af',
                'part_hist_ohrd',
                'part_hist_interv',
                'v1_sample_pregnant',
                'v1_sample_haem',
                'v1_sample_tra3m',
                'v1_blood_taken',
                'v1_taken_urine_sample',
                'v1_systolic',
                'v1_diastolic',
                'v1_hr',
                'v1_height',
                'v1_weight',
                'v1_bmi',
            ],
            [RECIPIENT_ADMIN]
        )


class IndapamideScreeningRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            SCREENING_PROJECT_ID,
            [
                'record_id',
                'pis',
                'protocol',
                'first_name',
                'last_name',
                'dob',
                'location',
                'consultant',
                'date_last_adm',
                'hf_type',
                'severity_lvef',
                'lvef',
                'severity_rv',
                'rv',
                'nyha',
                'bnp',
                'ntprobnp',
                'ferritin',
                'egfr',
                'cad_yn',
                'dil_cardiomypathy',
                'valve_hd_yn',
                'known_hypertension_yn',
                'known_hypotension_yn',
                'diabetes_yn',
                'asthma_yn',
                'device_yn',
                'arrhythmias_yn',
                'gout_yn',
                'indapamide_yn',
                'suit_for_hf_study_yn',
                'randomised_to',
            ],
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class IndapamideScreeningRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            SCREENING_PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            ['record_id'],
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidBloodPressureVisit1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            'v1_systolic',
            'v1_diastolic',
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidBloodPressureVisit2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            'v2_systolic',
            'v2_diastolic',
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidBloodPressureVisit3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            'v3_systolic',
            'v3_diastolic',
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidBloodPressureVisit4(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            'v4_systolic',
            'v4_diastolic',
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [
                'v1_hr',
                'v2_hr',
                'v3_hr',
                'v4_hr',
            ],
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            ['v1_height'],
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [
                'v1_weight',
                'v2_weight',
                'v3_weight',
                'v4_weight',
            ],
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            ['v1_bmi'],
            [RECIPIENT_ADMIN]
        )


class IndapamideRedcapCrfWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            CRF_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class IndapamideRedcapScreeningcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            SCREENING_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
