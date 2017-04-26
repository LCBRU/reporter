#!/usr/bin/env python3

import schedule
import time
from reporter.reports import *

while True:
    schedule.run_pending()
    time.sleep(1)