#!/usr/bin/env python3

from reporter.reports.dwbriccs.pmi import PmiPatientMismatch
from reporter.emailing import RECIPIENT_GENVASC_ADMIN


class GenvascPmiPatientMismatch(PmiPatientMismatch):
    def __init__(self):
        super().__init__(
            project='i2b2_app03_genvasc_Data',
            recipients=[RECIPIENT_GENVASC_ADMIN]
        )
