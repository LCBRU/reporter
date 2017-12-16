#!/usr/bin/env python3

import schedule
import time
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from reporter.reports import get_concrete_reports

logging.info("---- Finding Reports ----")

reports = get_concrete_reports()

for r in reports:
    r.schedule()
#    if type(r).__name__[:4] == 'Fast':
#        r.run()


logging.info("---- All reports scheduled ----")

while True:
    schedule.run_pending()
    time.sleep(1)
