#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_LENTEN_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_LENTEN_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.core import Schedule

REDCAP_PROJECT_ID = 25
REDCAP_INSTANCE = RedcapInstance.internal


class LentenRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Lenten',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LentenRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Lenten',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


class LentenRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
