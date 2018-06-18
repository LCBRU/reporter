#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.connections import DatabaseConnection
from reporter.connections import OpenSpecimenInstance
from reporter.emailing import (
    RECIPIENT_OPENSPECIMEN_MANAGER as RECIPIENT_OPENSPECIMEN_MANAGER,
)


class OpenSpecimenIdsMissing(SqlReport):
    def __init__(
        self,
        openspecimen_instance,
        recipients,
        schedule=None
    ):

        self._openspecimen_instance = openspecimen_instance
        super().__init__(
            introduction=("The following participants do not have "
                          "all required identifiers in OpenSpecimen"),
            recipients=recipients,
            schedule=schedule,
            conn=DatabaseConnection.uol_lamp,
            sql='''

SELECT
	u.LOGIN_NAME,
    p.EMPI_ID as master_patient_index,
    cpr.PROTOCOL_PARTICIPANT_ID AS protocol_participant_id,
    cpr.IDENTIFIER AS collection_protocol_reg_id,
    cpr.COLLECTION_PROTOCOL_ID AS collection_protocol_id
FROM catissue_participant p
JOIN	catissue_coll_prot_reg cpr
	ON cpr.PARTICIPANT_ID = p.IDENTIFIER
    AND cpr.ACTIVITY_STATUS = 'Active'
LEFT JOIN	catissue_specimen_coll_group scg
	ON scg.COLLECTION_PROTOCOL_REG_ID = cpr.IDENTIFIER
LEFT JOIN catissue_coll_prot_event cpe
	ON cpe.IDENTIFIER = scg.COLLECTION_PROTOCOL_EVENT_ID
LEFT JOIN	catissue_site s
	ON s.IDENTIFIER = scg.SITE_ID
LEFT JOIN catissue_participant_aud paud
	ON paud.IDENTIFIER = p.IDENTIFIER
    AND paud.REVTYPE = 0
LEFT JOIN os_revisions rev
	ON rev.REV = paud.REV
LEFT JOIN catissue_user u
	ON u.IDENTIFIER = rev.USER_ID
LEFT JOIN catissue_part_medical_id mid
	ON mid.PARTICIPANT_ID = p.IDENTIFIER
WHERE COALESCE(p.EMPI_ID, '') = ''
	AND COALESCE(cpr.PROTOCOL_PARTICIPANT_ID, '') = ''
ORDER BY u.LOGIN_NAME
;

                ''',
        )

    def get_report_line(self, row):
        errors = []
        if row['no_pmi'] == 1:
            errors.append('Patient Master Index')
        if row['no_ppi'] == 1:
            errors.append('Protocol Participant ID')

        messages = ', '.join(errors)

        return '- {}: Entered by {} is missing {}\r\n'.format(
            self._openspecimen_instance()['link_generator'](
                row['protocol_participant_id'] or row['master_patient_index'] or 'click here',
                row['collection_protocol_id'],
                row['collection_protocol_reg_id']),
            row['LOGIN_NAME'] or 'Unknown',
            messages,
        )


class AllOpenSpecimenIdsMissing(
    OpenSpecimenIdsMissing):

    def __init__(self):
        super().__init__(
            openspecimen_instance=OpenSpecimenInstance.live,
            recipients=[RECIPIENT_OPENSPECIMEN_MANAGER],
        )
