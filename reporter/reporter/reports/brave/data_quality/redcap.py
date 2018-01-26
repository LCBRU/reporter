#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRAVE_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_LEICESTER_PROJECT_ID = 25
REDCAP_KETTERING_PROJECT_ID = 28
REDCAP_LINCOLN_PROJECT_ID = 37
REDCAP_SHEFFIELD_PROJECT_ID = 54
REDCAP_IMPERIAL_PROJECT_ID = 56
REDCAP_GRANTHAM_PROJECT_ID = 59
REDCAP_WEST_SUFFOLK_PROJECT_ID = 60


class BraveRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class BraveRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class BraveRedcapLeicesterWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            REDCAP_LEICESTER_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BraveRedcapKetteringWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_KETTERING_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BraveRedcapLincolnWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_LINCOLN_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BraveRedcapSheffieldWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_SHEFFIELD_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BraveRedcapImperialWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_IMPERIAL_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BraveRedcapGranthamWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_GRANTHAM_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BraveRedcapWestSuffolkWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_WEST_SUFFOLK_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
