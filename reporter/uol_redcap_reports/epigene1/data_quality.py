#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_EPIGENE1_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_EPIGENE1_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidHeightInCm,
    RedcapInvalidPulse,
)

REDCAP_PROJECT_ID = 12


class EpiGene1RedcapStudyNumber(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^\d{3}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class EpiGene1RedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class EpiGene1RedcapInvalidHeightInCm(RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class EpiGene1RedcapInvalidWeightInKg(RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class EpiGene1RedcapInvalidBmi(RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['bmi_calc'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class EpiGene1RedcapInvalidPulse(RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=[
                'pre_op_hr',
                'cicu_hr',
                'h12_hr',
                'h24_hr',
                'h48_hr',
                'h72_hr',
                'h96_hr'
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
