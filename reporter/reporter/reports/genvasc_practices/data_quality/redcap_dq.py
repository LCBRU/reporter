#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.emailing import (
    RECIPIENT_GENVASC_MANAGER,
    RECIPIENT_GENVASC_ADMIN
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingData,
)


class GenvascPracticesRedcapMissingDataNorthants(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            29,
            [
                'practice_name',
                'practice_code',
            ],
            [RECIPIENT_GENVASC_ADMIN, RECIPIENT_GENVASC_MANAGER]
        )


class GenvascPracticesRedcapMissingDataLeicestershire(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            53,
            [
                'practice_name',
                'practice_code',
            ],
            [RECIPIENT_GENVASC_ADMIN, RECIPIENT_GENVASC_MANAGER]
        )
