#!/usr/bin/env python3

from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.emailing import (
    RECIPIENT_AS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_AS_MANAGER as RECIPIENT_MANAGER,
)


class AsRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'AS',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])
