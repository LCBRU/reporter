#!/usr/bin/env python3

from reporter.reports.databases import RedcapInstance
from reporter.reports.emailing import (
    RECIPIENT_CARDIOMET_ADMIN as RECIPIENT_ADMIN
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapInvalidStudyNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidNhsNumber,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
    RedcapInvalidEmailAddress,
    RedcapInvalidDate,
)

PROJECT_ID = 64


class CardiometDemographicsRedcapMissingData(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [
                'patient_id',
                'research_appt_date',
                'nhs_no',
                'first_name',
                'last_name',
                'dob',
                'add_1',
                'add_2',
                'add_3',
                'add_4',
                'postcode',
                'gender',
                'ethnicity',
            ],
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            ['patient_id'],
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapInvalidNhsNumber(
        RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            ['nhs_no'],
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            ['s_no'],
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            ['postcode'],
            [RECIPIENT_ADMIN]
        )


class CardiometDemographicsRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            PROJECT_ID,
            ['email_add'],
            [RECIPIENT_ADMIN]
        )
