#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.reports.emailing import (
    RECIPIENT_SCAD_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_SCAD_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_CLINICAL_VISIT_PROJECT_ID = 28
REDCAP_REGISTRY_PROJECT_ID = 31
REDCAP_INSTANCE = RedcapInstance.internal


class ScadRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'SCAD',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class ScadRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'SCAD',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class ScadRedcapClinicalVisitWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class ScadRedcapRegistryWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_REGISTRY_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
