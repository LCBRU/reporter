# BRC Email Reporter

This tool runs in the background and periodically runs data quality and
management information reports, which are emailed to the appropriate
recipient.

## Installation

1. Download the code from GutHub:

```bash
git clone https://github.com/LCBRU/reporter.git
```

2. Install the requirements:

Got to the reporter directory

```bash
pip install -r requirements.txt
```

3. Set environment:

Copy the file `example.env` to `.env` and fill in appropriate values.

## Running

Each system has a different application that imports the appropriate reports
and schedules them for running, but can also be used to run individual or
multiple reports.

### Scheduling reports

If no arguments are supplied to the application, all the reports will be
scheduled.  For example:

```bash
python uhl_reports.py
```

### Running all reports

To run all the imported reports, use the `-a` or `--all` command line
arguments.  For example:

```bash
python uhl_reports.py --all
```

### Running specific reports

To specify reports that you want to run, add their report class
name or part of their report class name as a command line argument.  Multiple
names or parts of names can be added.  The names do not need to match the
case of the report class name.  For example:

```bash
python uhl_reports.py redcap civicrm
```

### Exclude reports from running

To specify reports to exclude from running, add the `-x` or `--exclude`
command line argument, followed by the report class name or part thereof.
For example:

```bash
python uhl_reports.py -x pdf
```

## Development

## Creating Reports

To create a new report you must inherit from the `Report` class defined in the
`core.py` module or, more usually, a class inherited from it - for example `PdfReport` or `SqlReport` - and then provide appropriate parameters such as some SQL to the constructor and overriding the `get_report_line`,
`get_report_lines` or `get_report` functions.

## Getting the Reports imported

If you add a new report it will only be run if it successfully imported by
the application.  If your report is not being imported, follow this trouble-
shooting list:

1. Make sure the report is a descendent of the `Report` class defined in
`reporter\core.py`.
2. Make sure all directories contain a `__init__.py` file.
3. Make sure that the report class is in a directory beneath the
directory imported by the system application.
3. Make sure the directory imported by the system application itself contains
a `__init__.py` file that contains the following code:

```python
from reporter.core import import_sub_reports

import_sub_reports(__path__, __name__)

```

## Emailing Reports

Reports are emailed to lists of addresses for roles defined in
environment variables.  To see which environment variables are available,
see the `reporter\emailing.py` file.  The name of the appropriate role
or roles will be passed as a constructor argument to `Report` parent class.

All reports will be emailed to the `RECIPIENT_IT_DQ` environment variable
address list.  If no recipients have been defined, even in the
`RECIPIENT_IT_DQ` environment variable, the report will be emailed to the
`DEFAULT_RECIPIENT` environment variable list.

## Selenium Reports

Selenium is a library that facillitates webscraping by controlling headerless
instances of Chrome or Firefox browsers.  This can be used when direct data
access is impossible or where the web interface shows information not avaiable
elsewhere.

In order to use Selenium you need to make sure that a Selenium Grid in running
and accessible to the Email Reporting application and that the connection
details have been set in the appropriate environment variables.

See the `LCBRU/selenium_grid` repository on GitHub or the SeleniumGrid SOPs for information.

The `SeleniumGrid` class in the `report\selenium.py` file wraps access to the
Selenium Grid in a context manager for convenience.
