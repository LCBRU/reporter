#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_FAST_ADMIN,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapXrefMismatch,
)


class FastRedcapXrefMismatchPractice(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=43,
            field_name_a='practice_location',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=48,
            field_name_b='gp_practice',
            recipients=[RECIPIENT_FAST_ADMIN]
        )


class FastRedcapXrefMismatchInvitationGroup(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=43,
            field_name_a='invitation_grp',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=48,
            field_name_b='invitation_group',
            recipients=[RECIPIENT_FAST_ADMIN]
        )


class FastRedcapXrefMismatchNhsNumber(
        RedcapXrefMismatch):
    def __init__(self):
        super().__init__(
            redcap_instance_a=RedcapInstance.internal,
            project_id_a=43,
            field_name_a='nhs_number',
            redcap_instance_b=RedcapInstance.internal,
            project_id_b=48,
            field_name_b='nhs_no',
            recipients=[RECIPIENT_FAST_ADMIN]
        )
