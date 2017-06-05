#!/usr/bin/env python3

from reporter.reports import PmiPatientMismatch
from reporter import RECIPIENT_GENVASC_ADMIN


class GenvascPmiPatientMismatch(PmiPatientMismatch):
    def __init__(self):
        super().__init__(
            project='i2b2_app03_genvasc_Data',
            recipients=[RECIPIENT_GENVASC_ADMIN]
        )
