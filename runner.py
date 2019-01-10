#!/usr/bin/env python3

import logging
import argparse
from reporter.core import run_all, schedule_reports, run_reports, list_all
from dotenv import load_dotenv


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_parameters():
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
    parser.add_argument(
        "-l",
        "--list",
        help="list all reports",
        action="store_true",
    )

    args = parser.parse_args()

    return args


def run():
    load_dotenv()

    args = get_parameters()

    exclude = [x.lower() for x in args.exclude]

    if args.all:
        run_all(exclude)

        logging.info("---- All reports run ----")
    elif args.list:
        list_all()

    elif not args.report_names:
        schedule_reports()
    else:
        for report_name in args.report_names:
            run_reports(report_name, exclude)

        logging.info("---- All reports run ----")
