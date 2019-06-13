#!/usr/bin/env python3

from reporter.connections import DatabaseConnection
from reporter.core import SqlReport, Schedule
from reporter.emailing import (
    RECIPIENT_DESMOND_MANAGER,
)


class DesmondActivityReport(SqlReport):
    def __init__(self):
        super().__init__(
            introduction=("The latest information for the DESMOND submissions"),
            recipients=[RECIPIENT_DESMOND_MANAGER],
            schedule=Schedule.weekly,
            conn=DatabaseConnection.uol_lamp,
            sql='''

SELECT
	group_concat(CASE WHEN field_name = 'site_name' THEN value END) site_name,

	group_concat(CASE WHEN field_name = 'patients_referred_feb_18' THEN value END) patients_referred_feb_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_feb_18' THEN value END) att_a_desmond_course_feb_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_feb_18' THEN value END) number_of_dnas_feb_18,
	group_concat(CASE WHEN field_name = 'courses_available_feb_18' THEN value END) courses_available_feb_18,
    
	group_concat(CASE WHEN field_name = 'patients_referred_mar_18' THEN value END) patients_referred_mar_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_mar_18' THEN value END) att_a_desmond_course_mar_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_mar_18' THEN value END) number_of_dnas_mar_18,
	group_concat(CASE WHEN field_name = 'courses_available_mar_18' THEN value END) courses_available_mar_18,

	group_concat(CASE WHEN field_name = 'patients_referred_apr_18' THEN value END) patients_referred_apr_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_apr_18' THEN value END) att_a_desmond_course_apr_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_apr_18' THEN value END) number_of_dnas_apr_18,
	group_concat(CASE WHEN field_name = 'courses_available_apr_18' THEN value END) courses_available_apr_18,

	group_concat(CASE WHEN field_name = 'patients_referred_may_18' THEN value END) patients_referred_may_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_may_18' THEN value END) att_a_desmond_course_may_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_may_18' THEN value END) number_of_dnas_may_18,
	group_concat(CASE WHEN field_name = 'courses_available_may_18' THEN value END) courses_available_may_18,

	group_concat(CASE WHEN field_name = 'patients_referred_jun_18' THEN value END) patients_referred_jun_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_jun_18' THEN value END) att_a_desmond_course_jun_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_jun_18' THEN value END) number_of_dnas_jun_18,
	group_concat(CASE WHEN field_name = 'courses_available_jun_18' THEN value END) courses_available_jun_18,

	group_concat(CASE WHEN field_name = 'patients_referred_jul_18' THEN value END) patients_referred_jul_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_jul_18' THEN value END) att_a_desmond_course_jul_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_jul_18' THEN value END) number_of_dnas_jul_18,
	group_concat(CASE WHEN field_name = 'courses_available_jul_18' THEN value END) courses_available_jul_18,

	group_concat(CASE WHEN field_name = 'patients_referred_aug_18' THEN value END) patients_referred_aug_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_aug_18' THEN value END) att_a_desmond_course_aug_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_aug_18' THEN value END) number_of_dnas_aug_18,
	group_concat(CASE WHEN field_name = 'courses_available_aug_18' THEN value END) courses_available_aug_18,

	group_concat(CASE WHEN field_name = 'patients_referred_sep_18' THEN value END) patients_referred_sep_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_sep_18' THEN value END) att_a_desmond_course_sep_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_sep_18' THEN value END) number_of_dnas_sep_18,
	group_concat(CASE WHEN field_name = 'courses_available_sep_18' THEN value END) courses_available_sep_18,

	group_concat(CASE WHEN field_name = 'patients_referred_oct_18' THEN value END) patients_referred_oct_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_oct_18' THEN value END) att_a_desmond_course_oct_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_oct_18' THEN value END) number_of_dnas_oct_18,
	group_concat(CASE WHEN field_name = 'courses_available_oct_18' THEN value END) courses_available_oct_18,

	group_concat(CASE WHEN field_name = 'patients_referred_nov_18' THEN value END) patients_referred_nov_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_nov_18' THEN value END) att_a_desmond_course_nov_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_nov_18' THEN value END) number_of_dnas_nov_18,
	group_concat(CASE WHEN field_name = 'courses_available_nov_18' THEN value END) courses_available_nov_18,

	group_concat(CASE WHEN field_name = 'patients_referred_dec_18' THEN value END) patients_referred_dec_18,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_dec_18' THEN value END) att_a_desmond_course_dec_18,
	group_concat(CASE WHEN field_name = 'number_of_dnas_dec_18' THEN value END) number_of_dnas_dec_18,
	group_concat(CASE WHEN field_name = 'courses_available_dec_18' THEN value END) courses_available_dec_18,

	group_concat(CASE WHEN field_name = 'patients_referred_jan_19' THEN value END) patients_referred_jan_19,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_jan_19' THEN value END) att_a_desmond_course_jan_19,
	group_concat(CASE WHEN field_name = 'number_of_dnas_jan_19' THEN value END) number_of_dnas_jan_19,
	group_concat(CASE WHEN field_name = 'courses_available_jan_19' THEN value END) courses_available_jan_19,

	group_concat(CASE WHEN field_name = 'patients_referred_feb_19' THEN value END) patients_referred_feb_19,
	group_concat(CASE WHEN field_name = 'att_a_desmond_course_feb_19' THEN value END) att_a_desmond_course_feb_19,
	group_concat(CASE WHEN field_name = 'number_of_dnas_feb_19' THEN value END) number_of_dnas_feb_19,
	group_concat(CASE WHEN field_name = 'courses_available_feb_19' THEN value END) courses_available_feb_19

FROM redcap_data rc
WHERE rc.project_id = 16
GROUP BY rc.record
;

                '''
        )

    def get_report_line(self, row):
        markdown = ''

        markdown += "**{}**\r\n\r\n".format(row['site_name'])

        markdown += '''
Month  | Referrals | Attenndees | DNAs | Courses
------ | --------- | ---------- | ---- | -------
'''

        for m in ['feb_18', 'mar_18', 'apr_18', 'may_18',
                  'jun_18', 'jul_18', 'aug_18', 'sep_18',
                  'oct_18', 'nov_18', 'dec_18', 'jan_19', 'feb_19']:
            markdown += "{} | {} | {} | {} | {}\r\n".format(
                m.replace('_', ' ').title(),
                row['patients_referred_{}'.format(m)] or ' ',
                row['att_a_desmond_course_{}'.format(m)] or ' ',
                row['number_of_dnas_{}'.format(m)] or ' ',
                row['courses_available_{}'.format(m)] or ' ',
            )

        markdown += '\r\n'

        return markdown
