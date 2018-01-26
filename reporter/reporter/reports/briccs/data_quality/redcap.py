#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_BRICCS_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRICCS_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_LEICESTER_PROJECT_ID = 24
REDCAP_DONCASTER_PROJECT_ID = 13
REDCAP_SHEFFIELD_PROJECT_ID = 14
REDCAP_KETTERING_PROJECT_ID = 15
REDCAP_CHESTERFIELD_PROJECT_ID = 16
REDCAP_GRANTHAM_PROJECT_ID = 17
REDCAP_LINCOLN_PROJECT_ID = 18
REDCAP_NORTHAMPTON_PROJECT_ID = 19
REDCAP_DERBY_PROJECT_ID = 25
REDCAP_BOSTON_PROJECT_ID = 26
REDCAP_NOTTINGHAM_PROJECT_ID = 27


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


class BriccsRedcapLeicesterWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            REDCAP_LEICESTER_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapDoncasterWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_DONCASTER_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapSheffieldWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_SHEFFIELD_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapKetteringWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_KETTERING_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapChesterfieldWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_CHESTERFIELD_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapGranthamWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_GRANTHAM_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapLincolnWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_LINCOLN_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapNorthamptonWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_NORTHAMPTON_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapDerbyWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_DERBY_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapBostonWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_BOSTON_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class BriccsRedcapNottinghamWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_NOTTINGHAM_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
