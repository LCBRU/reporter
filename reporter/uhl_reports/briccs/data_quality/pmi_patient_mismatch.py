#!/usr/bin/env python3

from reporter.uhl_reports.dwbriccs.pmi import PmiPatientMismatch
from reporter.emailing import RECIPIENT_BRICCS_ADMIN


class BriccsPmiPatientMismatch(PmiPatientMismatch):
    def __init__(self):
        super().__init__(
            project='i2b2_app03_b1_Data',
            recipients=[RECIPIENT_BRICCS_ADMIN]
        )
