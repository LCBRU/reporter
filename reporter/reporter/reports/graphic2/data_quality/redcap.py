#!/usr/bin/env python3

from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_GRAPHIC2_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_GRAPHIC2_MANAGER as RECIPIENT_MANAGER,
)


class Graphic2RedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Graphic2',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class Graphic2RedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Graphic2',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])
