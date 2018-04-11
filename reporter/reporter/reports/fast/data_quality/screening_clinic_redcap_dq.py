#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingDataWhen,
    RedcapMissingAllWhen,
    RedcapInvalidNhsNumber,
    RedcapImpliesCheck,
    RedcapInvalidEmailAddress,
    RedcapInvalidDate,
    RedcapInvalidHeightInCm,
    RedcapInvalidHeightInFeetAndInches,
    RedcapInvalidWeightInKg,
    RedcapInvalidWeightInStonesAndPounds,
    RedcapInvalidPostCode,
)


class FastNotFemale(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['patient_reruited'],
            ['1'],
            ['gender'],
            ['0'],
            'Participant is not female',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['email_add'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['nhs_no'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['postcode'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapMissingDataWhenRecruited(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            [
                'first_name',
                'last_name',
                'postcode',
                'gp_practice',
                'clinic_date',
                'invitation_group',
                'patient_attend',
                'patient_agree_scan',
            ],
            'patient_reruited',
            '1',
            [RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN]
        )


class FastRedcapMissingAddressWhenRecruited(RedcapMissingAllWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['add_1', 'add_2', 'add_3', 'add_4'],
            'patient_reruited',
            '1',
            [RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN]
        )


class FastRedcapMissingHeightWhenRecruited(RedcapMissingAllWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['height_ft', 'height_inches', 'height_cms'],
            'patient_reruited',
            '1',
            [RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['height_cms'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidHeightInFeetAndInches(
        RedcapInvalidHeightInFeetAndInches):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            'height_ft',
            'height_inches',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapMissingWeightWhenRecruited(RedcapMissingAllWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['weight_stones', 'weight_pounds', 'weight_kgs'],
            'patient_reruited',
            '1',
            [RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            ['weight_kgs'],
            [RECIPIENT_FAST_ADMIN]
        )


class FastRedcapInvalidWeightInStonesAndPounds(
        RedcapInvalidWeightInStonesAndPounds):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            48,
            'weight_stones',
            'weight_pounds',
            [RECIPIENT_FAST_ADMIN]
        )
