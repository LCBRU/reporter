#!/usr/bin/env python3

from reporter.core import SqlReport
from reporter.connections import DatabaseConnection
from reporter.connections import OpenSpecimenInstance
from reporter.emailing import (
    RECIPIENT_OPENSPECIMEN_MANAGER as RECIPIENT_OPENSPECIMEN_MANAGER,
)


class OpenSpecimenPatientIdentifiableInformation(SqlReport):
    def __init__(
        self,
        openspecimen_instance,
        recipients,
        schedule=None
    ):

        self._openspecimen_instance = openspecimen_instance
        super().__init__(
            introduction=("The following participants potentially have "
                          "identifiable data in Open Specimen"),
            recipients=recipients,
            schedule=schedule,
            conn=DatabaseConnection.uol_lamp,
            sql='''

SELECT
	u.LOGIN_NAME,
    cpr.PROTOCOL_PARTICIPANT_ID AS protocol_participant_id,
    cpr.IDENTIFIER AS collection_protocol_reg_id,
    cpr.COLLECTION_PROTOCOL_ID AS collection_protocol_id,
	CASE WHEN COALESCE(p.LAST_NAME, '') <> ''
			OR COALESCE(p.FIRST_NAME, '') <> ''
			OR COALESCE(p.MIDDLE_NAME, '')
		THEN 1 ELSE 0 END AS with_name,
	CASE WHEN COALESCE(p.BIRTH_DATE, '') <> ''
		THEN 1 ELSE 0 END AS with_dob,
	CASE WHEN COALESCE(p.DEATH_DATE, '') <> ''
		THEN 1 ELSE 0 END AS with_death,
	CASE WHEN COALESCE(mid.MEDICAL_RECORD_NUMBER, '') <> ''
		THEN 1 ELSE 0 END AS with_medical_record_number,
	CASE WHEN COALESCE(p.GENDER, '') <> ''
		THEN 1 ELSE 0 END AS with_gender,
	CASE WHEN COALESCE(p.ETHNICITY, '') <> ''
		THEN 1 ELSE 0 END AS with_ethnicity,
	CASE WHEN COALESCE(p.SOCIAL_SECURITY_NUMBER, '') <> ''
		THEN 1 ELSE 0 END AS with_social_security_number
FROM catissue_participant p
JOIN	catissue_coll_prot_reg cpr
	ON cpr.PARTICIPANT_ID = p.IDENTIFIER
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
WHERE COALESCE(mid.MEDICAL_RECORD_NUMBER, '') <> ''
	OR COALESCE(p.LAST_NAME, '') <> ''
	OR COALESCE(p.FIRST_NAME, '') <> ''
	OR COALESCE(p.MIDDLE_NAME, '') <> ''
	OR COALESCE(p.BIRTH_DATE, '') <> ''
	OR COALESCE(p.DEATH_DATE, '') <> ''
	OR COALESCE(p.GENDER, 'Unspecified') <> 'Unspecified'
	OR COALESCE(p.ETHNICITY, 'Unknown') <> 'Unknown'
	OR COALESCE(p.SOCIAL_SECURITY_NUMBER, '') <> ''
ORDER BY u.LOGIN_NAME
;

                ''',
        )

    def get_report_line(self, row):
        errors = []
        if row['with_name'] == 1:
            errors.append('Names')
        if row['with_dob'] == 1:
            errors.append('Date of Birth')
        if row['with_medical_record_number'] == 1:
            errors.append('Medical Record Number')
        if row['with_gender'] == 1:
            errors.append('Gender')
        if row['with_ethnicity'] == 1:
            errors.append('Ethnicity')
        if row['with_social_security_number'] == 1:
            errors.append('Social Security Number')

        messages = ', '.join(errors)

        return '- {}: Entered by {} contains {}\r\n'.format(
            self._openspecimen_instance()['link_generator'](
                row['protocol_participant_id'] or 'click here',
                row['collection_protocol_id'],
                row['collection_protocol_reg_id']),
            row['LOGIN_NAME'] or 'Unknown',
            messages,
        )


class AllOpenSpecimenPatientIdentifiableInformation(
    OpenSpecimenPatientIdentifiableInformation):

    def __init__(self):
        super().__init__(
            openspecimen_instance=OpenSpecimenInstance.live,
            recipients=[RECIPIENT_OPENSPECIMEN_MANAGER],
        )


