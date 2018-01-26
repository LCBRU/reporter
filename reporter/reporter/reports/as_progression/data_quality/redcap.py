#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.emailing import (
    RECIPIENT_AS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_AS_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_PROJECT_ID = 37
REDCAP_INSTANCE = RedcapInstance.internal


class AsRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'AS',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class AsRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
