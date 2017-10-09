#!/usr/bin/env python3

from reporter.reports import Report, Schedule
from reporter import (
    RedcapInstance,
    RECIPIENT_FAST_ADMIN
)

# Abstract Reports


class RedcapImpliesCheck(Report):
    def __init__(
        self,
        redcap_instance,
        project_id,
        indicator_fields,
        indicator_values,
        consequence_fields,
        consequence_values,
        error_message,
        recipients,
        reverse=False,
        schedule=Schedule.monthly
    ):
        self._redcap_instance = redcap_instance
        self._error_message = error_message

        if reverse:
            comparison = "EXISTS"
        else:
            comparison = "NOT EXISTS"

        super().__init__(
            introduction=("The following participants have the following "
                          "invalid data in REDCap"),
            recipients=recipients,
            schedule=schedule,
            sql='''

SELECT
    a.record,
    a.project_id
FROM    {0}.dbo.redcap_data a
WHERE a.project_id = %s
    AND a.field_name IN ({1})
    AND a.value IN ({2})
    AND {5} (
        SELECT 1
        FROM    STG_redcap.dbo.redcap_data b
        WHERE b.project_id = a.project_id
            AND b.record = a.record
            AND b.field_name IN ({3})
            AND b.value IN ({4})
    )

                '''.format(
                redcap_instance()['staging_database'],
                ', '.join(['%s'] * len(indicator_fields)),
                ', '.join(['%s'] * len(indicator_values)),
                ', '.join(['%s'] * len(consequence_fields)),
                ', '.join(['%s'] * len(consequence_values)),
                comparison
            ),
            parameters=(tuple([project_id]) + tuple(indicator_fields) +
                        tuple(indicator_values) + tuple(consequence_fields) +
                        tuple(consequence_values))
        )

    def get_report_line(self, row):
        return '- {}: {}\r\n'.format(
            self._redcap_instance()['link_generator'](
                row['record'], row['project_id'], row['record']),
            self._error_message
        )


# FAST

class FastCurrentSmokerGroupButNotCurrentSmoker(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['0'],
            ['curr_smoke'],
            ['1'],
            'Participant in current smoker group, but is not a current smoker',
            [RECIPIENT_FAST_ADMIN]
        )


class FastExSmokerGroupButNotExSmoker(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['1'],
            ['ex_smoker'],
            ['1'],
            'Participant in Ex-smoker group, but is not an ex-smoker',
            [RECIPIENT_FAST_ADMIN]
        )


class FastRiskFactorGroupButNoRiskFactors(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['2'],
            ['diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol', 'fam_hist_aaa',
             'reg_meds'],
            ['1', '2', '3', '4'],
            'Participant in risk factor group, but is has no risk factors',
            [RECIPIENT_FAST_ADMIN]
        )


class FastNoRiskFactorGroupButHasRiskFactors(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['3'],
            ['diabetes', 'stroke', 'diag_mi', 'cabg', 'coronary_angio',
             'stents_balloons', 'narrow_arteries', 'diag_hypertension',
             'hypertension_med', 'diag_high_cholesterol',
             'reg_meds', 'curr_smoke', 'ex_smoker'],
            ['1', '2', '3', '4'],
            'Participant in no risk factors group, but is has risk factors',
            [RECIPIENT_FAST_ADMIN],
            True
        )


class FastEthnicMinorityGroupButNotInEthnicMinority(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['4'],
            ['ethnicity'],
            ['D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'],
            'Participant in ethinic minority group, '
            'but is not in an ethnic minority',
            [RECIPIENT_FAST_ADMIN]
        )


class FastSiblingsGroupButNoFamilyHistory(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['5'],
            ['fam_hist_aaa'],
            ['1'],
            'Participant in siblings group, but has no family history of AAA',
            [RECIPIENT_FAST_ADMIN]
        )


class FastWhiteEthnicGroupButInEthinicMinority(
        RedcapImpliesCheck):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            43,
            ['invitation_grp'],
            ['0', '1', '2', '3'],
            ['ethnicity'],
            ['D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S'],
            'Participant in white ethnic group, but in ethnic minority',
            [RECIPIENT_FAST_ADMIN],
            True
        )
