#!/usr/bin/env python3

import re
from reporter.core import SqlReport
from reporter.connections import RedcapInstance
from reporter.connections import DatabaseConnection
from reporter.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRAVE_MANAGER as RECIPIENT_MANAGER,
)

REDCAP_PROJECT_ID = 25

# Abstract Reports


class RedcapInvalidNhsNumber(SqlReport):
    def __init__(
        self,
        redcap_instance,
        project_id,
        fields,
        recipients,
        schedule=None
    ):

        self._redcap_instance = redcap_instance
        super().__init__(
            introduction=("The following participants an invalid NHS Number "
                          "in REDCap"),
            recipients=recipients,
            schedule=schedule,
            conn=DatabaseConnection.uol_lamp,
            sql='''

SELECT
    e.project_id,
    e.record,
    e.value,
    md.element_label
FROM redcap.redcap_data e
JOIN redcap.redcap_metadata md
    ON md.project_id = e.project_id
    AND md.field_name = e.field_name
WHERE e.project_id = %s
    AND e.field_name IN ('nhs_no')

                ''',
            parameters=(project_id)
        )

    def get_report_lines(self, cursor):
        markdown = ''
        errors = 0

        for row in cursor:
            if self.invalid_nhs_number(row['value']):
                markdown += self.get_report_line(row)
                errors += 1

        return markdown, errors

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            row['element_label']
        )

    def invalid_nhs_number(self, nhs_number):
        """
            Checks a given NHS numbers <string> is valid.
            @Returns: is_valid<bool>
        """
        # Nhs number is sometimes inputted xxx-xxx-xxxx, lets strip this down
        nhs_number = re.sub('[- ]', '', nhs_number)

        # A valid NHS number must be 10 digits long
        if not re.search(r'^[0-9]{10}$', nhs_number):
            return False

        checkcalc = lambda sum: 11 - (sum % 11)

        l = sum([int(j) * (11 - (i+1)) for i, j in enumerate(nhs_number[:-1])])
        checksum = checkcalc(l) if checkcalc(l) != 11 else 0

        return checksum != int(nhs_number[9])


class FoamiRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.uol_lamp,
            project_id=REDCAP_PROJECT_ID,
            fields=['nhs_num'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


