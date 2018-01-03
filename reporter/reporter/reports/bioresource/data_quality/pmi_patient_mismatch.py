#!/usr/bin/env python3

from reporter.reports.dwbriccs.pmi import PmiPatientMismatch
from reporter.reports.emailing import (
    RECIPIENT_BIORESOURCE_ADMIN,
    RECIPIENT_IT_DQ,
)


class BioresourcePmiPatientMismatch(PmiPatientMismatch):
    def __init__(self):
        super().__init__(
            project='i2b2_app03_bioresource_Data',
            recipients=[RECIPIENT_BIORESOURCE_ADMIN, RECIPIENT_IT_DQ]
        )
