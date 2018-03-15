#!/usr/bin/env python3

import schedule
import time
import logging
import argparse
import traceback


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from reporter.reports import get_concrete_reports
from reporter.reports.emailing import email_error


def schedule_reports():
    reports = get_concrete_reports()

    for r in reports:
        r.schedule()

    logging.info("---- All reports scheduled ----")

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception:
            logging.error(traceback.format_exc())
            email_error('Scheduled', traceback.format_exc())


def run_reports(report_name, exclude):
    reports = get_concrete_reports()

    for r in reports:

        if type(r).__name__.lower() in exclude:
            continue

        if type(r).__name__[:len(report_name)].lower() == report_name.lower():
            try:
                r.run()
            except Exception:
                logging.error(traceback.format_exc())
                email_error(r._name, traceback.format_exc())


def run_all(exclude):
    reports = get_concrete_reports()

    for r in reports:

        if type(r).__name__.lower() in exclude:
            continue

        r.run()


parser = argparse.ArgumentParser(description='Run specific reports.')
parser.add_argument(
    'report_names',
    metavar='report_names',
    nargs='*',
    help='Report names or start of the report name',
)
parser.add_argument(
    '-x',
    '--exclude',
    nargs='*',
    help='Reports names to exclude',
    default=[]
)
parser.add_argument(
    "-a",
    "--all",
    help="Run all reports",
    action="store_true",
)

args = parser.parse_args()

exclude = [x.lower() for x in args.exclude]

if args.all:
    run_all(exclude)

    logging.info("---- All reports run ----")
elif not args.report_names:
    schedule_reports()
else:
    for report_name in args.report_names:
        run_reports(report_name, exclude)

    logging.info("---- All reports run ----")
