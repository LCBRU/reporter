#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_TMAO_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_TMAO_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapMissingDataWhen,
    RedcapInvalidDate,
    RedcapFieldMatchesRegularExpression,
)
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.core import Schedule

REDCAP_PROJECT_ID = 25
REDCAP_INSTANCE = RedcapInstance.internal


class TmaoRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [
                'tmao_gender',
                'how_would_you_best_describ',
                'tmao_dob',
                'are_you_a_vegan',
                'do_you_take_nutritional_su',
                'how_many_per_times_week_do'
            ],
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapMissingDataWhenEatRedMeat(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [
                'how_many_times_per_week_do',
                'how_many_times_pork',
                'how_many_times_lamb'
            ],
            'do_you_eat_red_meat',
            '1',
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapMissingDataWhenNotVegan(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [
                'do_you_eat_eggs',
                'do_you_eat_red_meat'
            ],
            'are_you_a_vegan',
            '0',
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapMissingDataWhenEggEater(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [
                'how_many_eggs_in_a_week'
            ],
            'do_you_eat_eggs',
            '1',
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapInvalidStudyNumber(
        RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            ['record_id'],
            'TMAO\d{4}',
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'TMAO',
            [RECIPIENT_MANAGER, RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'TMAO',
            [RECIPIENT_MANAGER, RECIPIENT_ADMIN],
            schedule=Schedule.never,
        )


class TmaoRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )
