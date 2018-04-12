#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import RECIPIENT_LENTEN_ADMIN
from reporter.uhl_reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapInvalidStudyNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi
)


class LentenRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            [
                'record_id',
                's_number',
                'v1_visit_date',
                'age',
                'ethnicity',
                'gender'
            ],
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            ['record_id'],
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidBloodPressureVisit1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            'v1_bp1_sys',
            'v1_bp_dias',
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidBloodPressureVisit2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            'v2_bp1_sys',
            'v2_bp_dias',
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidBloodPressureVisit3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            'v3_bp1_sys',
            'v3_bp_dias',
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidBloodPressureVisit4(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            'v4_bp1_sys',
            'v4_bp_dias',
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidBloodPressureVisitUnscheduled(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            'bp1_sys_unsched',
            'bp_dias_unsched',
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            [
                'pulse1_unsched',
                'v4_pulse1',
                'v3_pulse1',
                'v2_pulse1',
                'v1_pulse1'
            ],
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            ['v1_height'],
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            [
                'v1_weight',
                'v2_weight',
                'v3_weight',
                'v4_weight',
                'weight_unsched'
            ],
            [RECIPIENT_LENTEN_ADMIN]
        )


class LentenRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            56,
            ['bmi'],
            [RECIPIENT_LENTEN_ADMIN]
        )
