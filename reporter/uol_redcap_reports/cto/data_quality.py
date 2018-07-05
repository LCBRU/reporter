#!/usr/bin/env python3

import re
from reporter.connections import RedcapInstance
from reporter.emailing import (
    RECIPIENT_FOAMI_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_FOAMI_MANAGER as RECIPIENT_MANAGER,
)
from reporter.application_abstract_reports.redcap.data_quality import (
    RedcapInvalidNhsNumber,
)

REDCAP_PROJECT_ID = 25
