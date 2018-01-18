#!/usr/bin/env python3

from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_BRICCS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRICCS_MANAGER as RECIPIENT_MANAGER,
)


class BriccsRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'BRICCS',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class BriccsRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'BRICCS',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])
