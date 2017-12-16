#!/usr/bin/env python3

import schedule
import time
import logging
import argparse

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from reporter.reports import get_concrete_reports


def schedule_reports():
    reports = get_concrete_reports()

    for r in reports:
        r.schedule()

    logging.info("Reports scheduled")

    while True:
        schedule.run_pending()
        time.sleep(1)

def run_reports(report_name):
    reports = get_concrete_reports()

    for r in reports:
        if type(r).__name__[:len(report_name)].lower() == report_name.lower():
            r.run()

    logging.info("Reports run")

parser = argparse.ArgumentParser(description='Run specific reports.')
parser.add_argument('report_name', metavar='report_name', nargs='?',
                   help='Report name or start of name')

args = parser.parse_args()

if (args.report_name is None):
    schedule_reports()
else:
    run_reports(args.report_name)

