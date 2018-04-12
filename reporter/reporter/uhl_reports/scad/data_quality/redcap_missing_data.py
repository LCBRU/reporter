#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import RECIPIENT_SCAD_ADMIN
from reporter.uhl_reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapInvalidDate,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidNhsNumber,
    RedcapInvalidUhlSystemNumber
)

# SCAD Clinical Visit


class ScadClinicalRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
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
                'study_status'
            ],
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicalRedcapInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            'part_bp1_sys',
            'part_bp_dias',
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicalRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            ['part_pulse1'],
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicalRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            ['part_height'],
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicalRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            ['part_weight'],
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicalRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            ['part_bmi'],
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadClinicalRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            28,
            [RECIPIENT_SCAD_ADMIN]
        )


# SCAD Registry & Screening Visit


class ScadRegistryRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            31,
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
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadRegistryInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            31,
            ['nhs_no'],
            [RECIPIENT_SCAD_ADMIN]
        )


class ScadRegistryInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            31,
            ['s_number'],
            [RECIPIENT_SCAD_ADMIN]
        )
