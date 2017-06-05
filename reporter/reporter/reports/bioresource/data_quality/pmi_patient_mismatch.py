#!/usr/bin/env python3

from reporter.reports import PmiPatientMismatch
from reporter import RECIPIENT_BIORESOURCE_ADMIN


class BioresourcePmiPatientMismatch(PmiPatientMismatch):
    def __init__(self):
        super().__init__(
            project='i2b2_app03_bioresource_Data',
            recipients=[RECIPIENT_BIORESOURCE_ADMIN]
        )
