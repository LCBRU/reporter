#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.reports.redcap.redcap_percentage_complete import (
    RedcapPercentageCompleteReport,
)
from reporter.reports.redcap.withdrawn_or_excluded_with_data import (
    RedcapWithdrawnOrExcludedWithDataReport,
)
from reporter.emailing import (
    RECIPIENT_BRAVE_ADMIN as RECIPIENT_ADMIN,
    RECIPIENT_BRAVE_MANAGER as RECIPIENT_MANAGER,
)
from reporter.reports.redcap.web_data_quality import (
    RedcapWebDataQuality,
)
from reporter.reports.redcap.data_quality import (
    RedcapInvalidNhsNumber,
    RedcapInvalidDate,
    RedcapInvalidStudyNumber,
    RedcapRecordInvalidStudyNumber,
    RedcapInvalidBloodPressure,
    RedcapInvalidPulse,
    RedcapInvalidHeightInCm,
    RedcapInvalidWeightInKg,
    RedcapInvalidBmi,
    RedcapInvalidUhlSystemNumber,
    RedcapInvalidPostCode,
    RedcapInvalidEmailAddress,
)

REDCAP_LEICESTER_PROJECT_ID = 25
REDCAP_KETTERING_PROJECT_ID = 28
REDCAP_LINCOLN_PROJECT_ID = 37
REDCAP_SHEFFIELD_PROJECT_ID = 54
REDCAP_IMPERIAL_PROJECT_ID = 56
REDCAP_GRANTHAM_PROJECT_ID = 59
REDCAP_WEST_SUFFOLK_PROJECT_ID = 60


class BraveRedcapPercentageCompleteReport(RedcapPercentageCompleteReport):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


class BraveRedcapWithdrawnOrExcludedWithDataReport(
        RedcapWithdrawnOrExcludedWithDataReport):
    def __init__(self):
        super().__init__(
            'BRAVE',
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER])


# Leicester

class BraveRedcapLeicesterWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.internal,
            REDCAP_LEICESTER_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLeicesterRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.internal,
            project_id=REDCAP_LEICESTER_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Kettering

class BraveRedcapKetteringWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_KETTERING_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveKetteringRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_KETTERING_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Lincoln

class BraveRedcapLincolnWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_LINCOLN_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveLincolnRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_LINCOLN_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Sheffield

class BraveRedcapSheffieldWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_SHEFFIELD_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveSheffieldRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_SHEFFIELD_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Imperial

class BraveRedcapImperialWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_IMPERIAL_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveImperialRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_IMPERIAL_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# Grantham

class BraveRedcapGranthamWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_GRANTHAM_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveGranthamRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_GRANTHAM_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


# West Suffolk

class BraveRedcapWestSuffolkWebDataQuality(RedcapWebDataQuality):
    def __init__(self):
        super().__init__(
            RedcapInstance.external,
            REDCAP_WEST_SUFFOLK_PROJECT_ID,
            [RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidNhsNumber(RedcapInvalidNhsNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['nhs_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidUhlSystemNumber(
        RedcapInvalidUhlSystemNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['s_number'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidDate(
        RedcapInvalidDate):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidStudyNumber(
        RedcapInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['record_id', 'briccs_id'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapRecordInvalidStudyNumber(
        RedcapRecordInvalidStudyNumber):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidPostCode(
        RedcapInvalidPostCode):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['address_postcode'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidEmailAddress(
        RedcapInvalidEmailAddress):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=[
                'pat_email1',
                'pat_email2',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidBloodPressure1(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            systolic_field_name='part_bp1_sys',
            diastolic_field_name='part_bp_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidBloodPressure2(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            systolic_field_name='part_bp2_sys',
            diastolic_field_name='part_bp2_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidBloodPressure3(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            systolic_field_name='part_bp3_sys',
            diastolic_field_name='part_bp3_dias',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidBloodPressureAvg(
        RedcapInvalidBloodPressure):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            systolic_field_name='part_avg_sys_bp',
            diastolic_field_name='part_avg_dias_bp',
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidPulse(
        RedcapInvalidPulse):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=[
                'part_pulse1',
                'part_pulse2',
                'part_pulse3',
                'avg_pulse',
            ],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidHeightInCm(
        RedcapInvalidHeightInCm):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['part_height'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidWeightInKg(
        RedcapInvalidWeightInKg):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['part_weight'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )


class BraveWestSuffolkRedcapInvalidBmi(
        RedcapInvalidBmi):
    def __init__(self):
        super().__init__(
            redcap_instance=RedcapInstance.external,
            project_id=REDCAP_WEST_SUFFOLK_PROJECT_ID,
            fields=['part_bmi'],
            recipients=[RECIPIENT_ADMIN, RECIPIENT_MANAGER],
        )
