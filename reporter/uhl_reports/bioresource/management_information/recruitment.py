#!/usr/bin/env python3

from reporter.core import Schedule
from reporter.uhl_reports.i2b2.recruitment import (
    CumulativeRecruitment,
)
from reporter.emailing import (
    RECIPIENT_BIORESOURCE_MANAGER as RECIPIENT_MANAGER,
)


I2B2_DB = "i2b2_app03_bioresource_Data"


class BioresourceCumulativeRecruitment(
        CumulativeRecruitment):
    def __init__(self):
        super().__init__(
            database=I2B2_DB,
            recipients=[RECIPIENT_MANAGER],
            schedule=Schedule.never,
        )
