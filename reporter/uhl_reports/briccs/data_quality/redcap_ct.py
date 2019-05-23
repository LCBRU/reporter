#!/usr/bin/env python3

from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_BRICCS_MANAGER,
    RECIPIENT_BRICCSCT_ANALYSERS,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapMissingDataWhen,
)

REDCAP_LEICESTER_PROJECT_ID = 24
REDCAP_KETTERING_PROJECT_ID = 15

class BriccsCtLeicesterRedcapCtAnalysedButDataMissing(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=[
                'ct_calcium_score_lms',
                'ct_calcium_score_lad',
                'ct_calcium_score_circum',
                'ct_calcium_score_rca',
                'ct_date_time_start',
            ],
            indicator_field='cardiac_imaging_data_complete',
            indicator_value='2',
            recipients=[RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCSCT_ANALYSERS],
        )


class BriccsCtKetteringRedcapCtAnalysedButDataMissing(
        RedcapMissingDataWhen):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=[
                'ct_calcium_score_lms',
                'ct_calcium_score_lad',
                'ct_calcium_score_circum',
                'ct_calcium_score_rca',
                'ct_date_time_start',
            ],
            indicator_field='cardiac_imaging_data_complete',
            indicator_value='2',
            recipients=[RECIPIENT_BRICCS_MANAGER, RECIPIENT_BRICCSCT_ANALYSERS],
        )
