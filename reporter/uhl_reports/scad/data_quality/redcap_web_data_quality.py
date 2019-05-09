#!/usr/bin/env python3

from reporter.core import Schedule
from reporter.connections import RedcapInstance
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_SCAD_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_SCAD_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
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
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
            Schedule.never,
        )


class ScadRedcapClinicalVisitWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_CLINICAL_VISIT_PROJECT_ID,
            [RECIPIENT_IT_DQ],
        )


class ScadRedcapRegistryWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_REGISTRY_PROJECT_ID,
            [RECIPIENT_IT_DQ],
        )
