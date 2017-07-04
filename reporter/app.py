#!/usr/bin/env python3

import schedule
import time
import logging
from reporter.reports import *


def get_concrete_reports(cls=None):

    if (cls is None):
        cls = Report

    result = [sub() for sub in cls.__subclasses__()
              if len(sub.__subclasses__()) == 0]

    for sub in [sub for sub in cls.__subclasses__()
                if len(sub.__subclasses__()) != 0]:
        result += get_concrete_reports(sub)

    return result


reports = get_concrete_reports()

for r in reports:
    r.schedule()
    # r.run()

logging.info("---- All reports scheduled ----")

while True:
    schedule.run_pending()
    time.sleep(1)
