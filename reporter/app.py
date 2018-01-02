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

    logging.info("---- All reports scheduled ----")

    while True:
        schedule.run_pending()
        time.sleep(1)


def run_reports(report_name):
    reports = get_concrete_reports()

    for r in reports:
        if type(r).__name__[:len(report_name)].lower() == report_name.lower():
            r.run()


parser = argparse.ArgumentParser(description='Run specific reports.')
parser.add_argument(
    'report_names',
    metavar='report_names',
    nargs='*',
    help='Report names or start of the report name'
)

args = parser.parse_args()

if (args.report_names is None):
    schedule_reports()
else:
    for report_name in args.report_names:
        run_reports(report_name)

    logging.info("---- All reports run ----")
