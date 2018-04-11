#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import (
    RECIPIENT_GENVASC_MANAGER as RECIPIENT_MANAGER,
    RECIPIENT_GENVASC_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_IT_DQ,
)
from reporter.reports.redcap.data_quality import (
    RedcapMissingData,
    RedcapInvalidEmailAddress,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)

REDCAP_NORTHANTS_PROJECT_ID = 29
REDCAP_LEICESTERS_PROJECT_ID = 53
REDCAP_INSTANCE = RedcapInstance.external


class GenvascPracticesRedcapMissingDataNorthants(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_NORTHANTS_PROJECT_ID,
            [
                'practice_name',
                'practice_code',
            ],
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER]
        )


class GenvascPracticesRedcapMissingDataLeicestershire(
        RedcapMissingData):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_LEICESTERS_PROJECT_ID,
            [
                'practice_name',
                'practice_code',
            ],
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER]
        )


class GenvascRedcapNorthantsWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_NORTHANTS_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class GenvascRedcapLeicestersWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            REDCAP_INSTANCE,
            REDCAP_LEICESTERS_PROJECT_ID,
            [RECIPIENT_IT_DQ]
        )


class GenvascLeicesterRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_LEICESTERS_PROJECT_ID,
            fields=[
                'loc_lead_email',
                'local_contact_email',
                'practice_manager_email',
                'sen_part_email',
                'contact_email_add',
            ],
            recipients=[RECIPIENT_IT_DQ],
        )


class GenvascNorthantsRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=REDCAP_INSTANCE,
            project_id=REDCAP_NORTHANTS_PROJECT_ID,
            fields=[
                'loc_lead_email',
                'local_contact_email',
                'practice_manager_email',
                'sen_part_email',
                'contact_email_add',
            ],
            recipients=[RECIPIENT_IT_DQ],
        )
