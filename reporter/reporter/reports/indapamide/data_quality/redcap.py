#!/usr/bin/env python3

from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_INDAPAMIDE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_INDAPAMIDE_MANAGER as RECIPIENT_MANAGER,
)


class IndapamideRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Indapamide',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class IndapamideRedcapWithdrawnOrExcludedWithDataReport(RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Indapamide',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])
