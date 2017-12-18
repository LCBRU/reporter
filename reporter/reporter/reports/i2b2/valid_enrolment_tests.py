#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter.reports.emailing import (
    RECIPIENT_BIORESOURCE_ADMIN,
    RECIPIENT_BRICCS_ADMIN
)
from reporter.reports.civicrm import get_case_link, get_contact_link


class StudyIdDuplicates(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following recruited participants have "
                          "duplicated study ids"),
            recipients=recipients,
            schedule=schedule,
            sql='''
        SELECT
            StudyNumber,
            CaseId,
            CiviCrmId
        FROM {0}.dbo.LOAD_ValidEnrollments
        WHERE StudyNumber IN (
            SELECT StudyNumber
            FROM {0}.dbo.LOAD_ValidEnrollments
            GROUP BY StudyNumber
            HAVING COUNT(*) > 1
        )
        ORDER BY StudyNumber
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_case_link(
                row['StudyNumber'],
                row["CaseId"],
                row["CiviCrmId"]))


class ContactMultipleRecruitments(Report):
    def __init__(self, database, recipients, schedule=None):
        super().__init__(
            introduction=("The following participants have multiple "
                          "recruited enrolments"),
            recipients=recipients,
            schedule=schedule,
            sql='''
            SELECT CiviCrmId
            FROM {}.dbo.LOAD_ValidEnrollments
            GROUP BY CiviCrmId
            HAVING COUNT(*) > 1
                '''.format(database)
        )

    def get_report_line(self, row):
        return '- {}\r\n\r\n'.format(
            get_contact_link('Click to View', row["CiviCrmId"]))


# Bioresource

class BioresourceStudyIdDuplicates(
        StudyIdDuplicates):
    def __init__(self):
        super().__init__(
            'i2b2_app03_bioresource_Data',
            [RECIPIENT_BIORESOURCE_ADMIN])


class BioresourceContactMultipleRecruitments(
        ContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            'i2b2_app03_bioresource_Data',
            [RECIPIENT_BIORESOURCE_ADMIN])


# BRICCS

class BriccsStudyIdDuplicates(
        StudyIdDuplicates):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            [RECIPIENT_BRICCS_ADMIN])


class BriccsContactMultipleRecruitments(
        ContactMultipleRecruitments):
    def __init__(self):
        super().__init__(
            'i2b2_app03_b1_Data',
            [RECIPIENT_BRICCS_ADMIN])
