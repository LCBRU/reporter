#!/usr/bin/env python3

from reporter.reports.i2b2.recruitment import (
    CumulativeRecruitment,
)
from reporter.reports.emailing import (
    RECIPIENT_GENVASC_MANAGER as RECIPIENT_MANAGER,
)


I2B2_DB = "i2b2_app03_genvasc_Data"


class BriccsCumulativeRecruitment(
        CumulativeRecruitment):
    def __init__(self):
        super().__init__(
            I2B2_DB,
            [RECIPIENT_MANAGER]
        )
