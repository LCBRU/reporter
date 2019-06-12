#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_LIMB_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_LIMB_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapFieldMatchesRegularExpression,
    RedcapInvalidDate,
    RedcapInvalidNhsNumber,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
    RedcapInvalidEmailAddress,
)

REDCAP_PROJECT_ID = 34


class LimbDemographicsRedcapStudyNumber(RedcapFieldMatchesRegularExpression):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['record_id'],
            regular_expression='^[A-Z]{2}\d{4}$',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbDemographicsRedcapInvalidDate(RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbDemographicsRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['nhs_no'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbDemographicsRedcapInvalidUhlSystemNumber(RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['s_no'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbDemographicsRedcapInvalidPostCode(RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['postcode', 'gp_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class LimbDemographicsRedcapInvalidEmailAddress(RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['email_add'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
