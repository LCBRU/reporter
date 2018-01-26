#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_BIORESOURCE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BIORESOURCE_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_PROJECT_ID = 9
REDCAP_INSTANCE = RedcapInstance.internal


class BioresRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'Bioresource',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class BioresourceRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'Bioresource',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class BioresourceRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
