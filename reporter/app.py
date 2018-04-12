#!/usr/bin/env python3

import logging
import argparse
import reporter.uhl_reports
from reporter.core import run_all, schedule_reports, run_reports

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
