#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.emailing import (
    RECIPIENT_TMAO_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_TMAO_MANAGER as RECIPIENT_MANAGER,
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapMissingDataWhen,
    RedcapInvalidStudyNumber,
    RedcapInvalidDate
)
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
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
            [RECIPIENT_ADMIN]
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
            [RECIPIENT_ADMIN]
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
            [RECIPIENT_ADMIN]
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
            [RECIPIENT_ADMIN]
        )


class TmaoRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            ['record_id'],
            [RECIPIENT_ADMIN]
        )


class TmaoRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            25,
            [RECIPIENT_ADMIN]
        )


class TmaoRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'TMAO',
            [RECIPIENT_MANAGER, RECIPIENT_ADMIN])


class TmaoRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'TMAO',
            [RECIPIENT_MANAGER, RECIPIENT_ADMIN])
