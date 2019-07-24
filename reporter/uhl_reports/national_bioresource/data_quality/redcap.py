#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.application_abstract_reports.redcap.percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.application_abstract_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_BIORESOURCE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BIORESOURCE_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.application_abstract_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapInvalidDate,
    RedcapInvalidStudyNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidHeightInCm,
    RedcapInvalidHeightInFeetAndInches,
    RedcapInvalidWeightInKg,
    RedcapInvalidWeightInStonesAndPounds,
)

REDCAP_PROJECT_ID = 9
REDCAP_INSTANCE = RedcapInstance.internal


class NationalBioresRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            study_name='Bioresource',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER]
        )


class NationalBioresourceRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='Bioresource',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER]
        )


class NationalBioresourceRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class NationalBioresourceRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN]
        )


class NationalBioresourceRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            recipients=[RECIPIENT_ADMIN]
        )


class NationalBioresourceRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN]
        )


class NationalBioresourceRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            fields=['your_height_centimetres'],
            recipients=[RECIPIENT_ADMIN]
        )


class NationalBioresourceRedcapInvalidHeightInFeetAndInches(
        RedcapInvalidHeightInFeetAndInches):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            feet_field='your_height_feet',
            inches_field='your_height_inches',
            recipients=[RECIPIENT_ADMIN]
        )


class NationalBioresourceRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            fields=['your_weight_kg'],
            recipients=[RECIPIENT_ADMIN]
        )


class NationalBioresourceRedcapInvalidWeightInStonesAndPounds(
        RedcapInvalidWeightInStonesAndPounds):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            stones_field='your_weight_stones',
            pounds_field='your_weight_pounds',
            recipients=[RECIPIENT_ADMIN]
        )
