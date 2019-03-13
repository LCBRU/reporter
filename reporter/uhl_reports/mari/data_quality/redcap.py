#!/usr/bin/env python3

from reporter.core import Schedule
from reporter.connections import RedcapInstance
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_MARI_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_MARI_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_NORTH_MIDS_PROJECT_ID = 30
REDCAP_COV_PROJECT_ID = 31
REDCAP_QUEEN_ELIZABETH_PROJECT_ID = 32
REDCAP_DUDLEY_PROJECT_ID = 33
REDCAP_WORCHESTER_PROJECT_ID = 34
REDCAP_CAMBRIDGE_PROJECT_ID = 35
REDCAP_HEART_OF_ENGLAND_PROJECT_ID = 36
REDCAP_HULL_PROJECT_ID = 55
REDCAP_GWENT_PROJECT_ID = 57
REDCAP_NORFOLK_PROJECT_ID = 58
REDCAP_INSTANCE = RedcapInstance.external


class MariRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Mari',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


class MariRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Mari',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


class MariRedcapNorthMidsWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_NORTH_MIDS_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapCoventryWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_COV_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapQueenElizabethWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_QUEEN_ELIZABETH_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapDudleyWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_DUDLEY_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapWorchesterWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_WORCHESTER_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapCambridgeWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CAMBRIDGE_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapHeartOfEnglandWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_HEART_OF_ENGLAND_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapHullWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_HULL_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapGwentWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_GWENT_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )


class MariRedcapNorfolkWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_NORFOLK_PROJECT_ID,
            [RECIPIENT_IT_DQ],
            schedule=Schedule.never,
        )
