#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.emailing import (
    RECIPIENT_CARDIOMET_ADMIN as RECIPIENT_ADMIN
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

PROJECT_ID = 67


class CardiometCrfRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [
                'record_id',
                'participant_group',
                'initials',
            ],
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            ['record_id'],
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureVisit1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'v1_bp1_sys',
            'v1_bp1_dias',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureRest(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'rest_systolic_bp',
            'rest_diastolic_bp',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureDobutamine(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'dobutamine_systolic_bp',
            'dobutamine_diastolic_bp',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureVisit2_1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'v2_bp1_sys',
            'v2_bp1_dias',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureVisit2_2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'v2_bp2_sys',
            'v2_bp2_dias',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureVisit2_3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'v2_bp3_sys',
            'v2_bp3_dias',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBloodPressureVisit2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            'v2_bp_sys',
            'v2_bp_dias',
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [
                'v2_pulse1',
                'v1_heart_rate1',
                'rest_heart_rate',
                'dobutamine_heart_rate',
                'v2_heart_rate1',
                'v2_heart_rate2',
                'v2_heart_rate3',
            ],
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [
                'v1_height',
                'v2_height',
            ],
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [
                'v1_weight',
                'v2_weight',
            ],
            [RECIPIENT_ADMIN]
        )


class CardiometCrfRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [
                'v1_bmi',
                'v2_bmi',
            ],
            [RECIPIENT_ADMIN]
        )
