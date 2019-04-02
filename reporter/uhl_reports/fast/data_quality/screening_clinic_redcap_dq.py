#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_FAST_MANAGER,
    RECIPIENT_FAST_ADMIN,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapMissingDataWhen,
    RedcapMissingAllWhen,
    RedcapInvalidNhsNumber,
    RedcapImpliesCheck,
    RedcapInvalidEmailAddress,
    RedcapInvalidDate,
    RedcapInvalidHeightInCm,
    RedcapInvalidHeightInFeetAndInches,
    RedcapInvalidWeightInKg,
    RedcapInvalidWeightInStonesAndPounds,
    RedcapInvalidPostCode,
)

REDCAP_SCREENING_PROJECT_ID = 48
REDCAP_INSTANCE = RedcapInstance.internal


class FastRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=['email_add'],
            recipients=[RECIPIENT_FAST_ADMIN],
        )


class FastScreeningRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            recipients=[RECIPIENT_FAST_ADMIN],
        )


class FastScreeningRedcapInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=['nhs_no'],
            recipients=[RECIPIENT_FAST_ADMIN],
        )


class FastRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=['postcode'],
            recipients=[RECIPIENT_FAST_ADMIN],
        )


class FastRedcapMissingDataWhenRecruited(RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=[
                'first_name',
                'last_name',
                'postcode',
                'gp_practice',
                'clinic_date',
                'invitation_group',
                'patient_attend',
                'patient_agree_scan',
            ],
            indicator_field='patient_recruited',
            indicator_value='1',
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
        )


class FastRedcapMissingAddressWhenRecruited(RedcapMissingAllWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_SCREENING_PROJECT_ID,
            fields=['add_1', 'add_2', 'add_3', 'add_4'],
            indicator_field='patient_recruited',
            indicator_value='1',
            recipients=[RECIPIENT_FAST_MANAGER, RECIPIENT_FAST_ADMIN],
        )
