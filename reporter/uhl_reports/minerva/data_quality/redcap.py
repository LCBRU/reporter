#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_MINERVA_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_MINERVA_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInM,
    RedcapInvalidWeightInKg,
    RedcapInvalidDate,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

GLENFIELD_PROJECT_ID = 53
REDCAP_INSTANCE = RedcapInstance.internal


class MinervaRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            study_name='MINERVA',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class MinervaRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='MINERVA',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER])

# Glenfield


class MinervaRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=GLENFIELD_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN]
        )


class MinervaRedcapInvalidBloodPressure(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=GLENFIELD_PROJECT_ID,
            systolic_field_name='systolic',
            diastolic_field_name='diastolic',
            recipients=[RECIPIENT_ADMIN]
        )


class MinervaRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=GLENFIELD_PROJECT_ID,
            fields=[
                'pulse',
            ],
            recipients=[RECIPIENT_ADMIN]
        )


class MinervaRedcapInvalidHeightInM(
        RedcapInvalidHeightInM):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=GLENFIELD_PROJECT_ID,
            fields=['height'],
            recipients=[RECIPIENT_ADMIN]
        )


class MinervaRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=GLENFIELD_PROJECT_ID,
            fields=[
                'weight',
            ],
            recipients=[RECIPIENT_ADMIN]
        )


class MinervaRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            GLENFIELD_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )
