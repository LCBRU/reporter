#!/usr/bin/env python3

from reporter.core import Schedule
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.emailing import (
    RECIPIENT_DREAM_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_DREAM_MANAGER as RECIPIENT_MANAGER,
)


class DreamRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'DREAM',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )


class DreamRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'DREAM',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])
