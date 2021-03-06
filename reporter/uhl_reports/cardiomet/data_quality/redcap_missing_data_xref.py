#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_CARDIOMET_ADMIN as RECIPIENT_ADMIN
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapXrefMismatch,
)

CRF_PROJECT_ID = 67
DEMOGRAPHICS_PROJECT_ID = 64


class CardiometCrfRedcapXrefMismatchDateOfBirth(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='dob',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='dob',
            recipients=[RECIPIENT_ADMIN],
        )


class CardiometCrfRedcapXrefMismatchGender(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='gender',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='gender',
            recipients=[RECIPIENT_ADMIN],
        )


class CardiometCrfRedcapXrefMismatchEthnicity(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=CRF_PROJECT_ID,
            field_name_a='ethnicity',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=DEMOGRAPHICS_PROJECT_ID,
            field_name_b='ethnicity',
            recipients=[RECIPIENT_ADMIN],
        )
