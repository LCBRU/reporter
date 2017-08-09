#!/usr/bin/env python3

from reporter.reports import PmiPatientMismatch, Schedule
from reporter import RECIPIENT_BRICCS_ADMIN


class BriccsPmiPatientMismatch(PmiPatientMismatch):
    def __init__(self):
        super().__init__(
            project='i2b2_app03_b1_Data',
            schedule=Schedule.never,
            recipients=[RECIPIENT_BRICCS_ADMIN]
        )