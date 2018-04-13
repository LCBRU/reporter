#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.uhl_reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.uhl_reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_BIORESOURCE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BIORESOURCE_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_IT_DQ,
)
from reporter.uhl_reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.uhl_reports.redcap.data_quality import (
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


class BioresRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            study_name='Bioresource',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER]
        )


class BioresourceRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            study_name='Bioresource',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER]
        )


class BioresourceRedcapWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_IT_DQ]
        )


class BioresourceRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN]
        )


class BioresourceRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            recipients=[RECIPIENT_ADMIN]
        )


class BioresourceRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN]
        )


class BioresourceRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            fields=['your_height_centimetres'],
            recipients=[RECIPIENT_ADMIN]
        )


class BioresourceRedcapInvalidHeightInFeetAndInches(
        RedcapInvalidHeightInFeetAndInches):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            feet_field='your_height_feet',
            inches_field='your_height_inches',
            recipients=[RECIPIENT_ADMIN]
        )


class BioresourceRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            fields=['your_weight_kg'],
            recipients=[RECIPIENT_ADMIN]
        )


class BioresourceRedcapInvalidWeightInStonesAndPounds(
        RedcapInvalidWeightInStonesAndPounds):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_PROJECT_ID,
            stones_field='your_weight_stones',
            pounds_field='your_weight_pounds',
            recipients=[RECIPIENT_ADMIN]
        )
