#!/usr/bin/env python3

from reporter import (
    RedcapInstance,
    RECIPIENT_TMAO_ADMIN
)
from reporter.reports.redcap.missing_data import (
    RedcapMissingData,
    RedcapMissingDataWhen,
    RedcapInvalidStudyNumber,
    RedcapInvalidDate
)


class TmaoRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            [
                'tmao_gender',
                'how_would_you_best_describ',
                'tmao_dob',
                'are_you_a_vegan',
                'do_you_take_nutritional_su',
                'how_many_per_times_week_do'
            ],
            [RECIPIENT_TMAO_ADMIN]
        )


class TmaoRedcapMissingDataWhenEatRedMeat(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            [
                'how_many_times_per_week_do',
                'how_many_times_pork',
                'how_many_times_lamb'
            ],
            'do_you_eat_red_meat',
            '1',
            [RECIPIENT_TMAO_ADMIN]
        )


class TmaoRedcapMissingDataWhenNotVegan(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            [
                'do_you_eat_eggs',
                'do_you_eat_red_meat'
            ],
            'are_you_a_vegan',
            '0',
            [RECIPIENT_TMAO_ADMIN]
        )


class TmaoRedcapMissingDataWhenEggEater(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            [
                'how_many_eggs_in_a_week'
            ],
            'do_you_eat_eggs',
            '1',
            [RECIPIENT_TMAO_ADMIN]
        )


class TmaoRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            ['record_id'],
            [RECIPIENT_TMAO_ADMIN]
        )


class TmaoRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            ['tmao_dob'],
            [RECIPIENT_TMAO_ADMIN]
        )
