#!/usr/bin/env python3

from reporter.databases import RedcapInstance
from reporter.emailing import RECIPIENT_BRICCS_ADMIN
from reporter.reports.redcap.data_quality import RedcapMissingAllWhen

# Abstract Classes


class BriccsRedcapBloodSamplesMissing(
        RedcapMissingAllWhen):
    def __init__(
        self,
        redcap_instance,
        project_id
    ):
        super().__init__(
            redcap_instance,
            project_id,
            [
                'blood_tube1',
                'blood_tube2',
                'blood_tube3',
                'blood_tube4',
                'blood_tube5',
            ],
            'blood_taken',
            '1',
            [RECIPIENT_BRICCS_ADMIN]
        )


class BriccsRedcapUrineSamplesMissing(
        RedcapMissingAllWhen):
    def __init__(
        self,
        redcap_instance,
        project_id
    ):
        super().__init__(
            redcap_instance,
            project_id,
            [
                'urine_sample',
            ],
            'taken_urine_sample',
            '1',
            [RECIPIENT_BRICCS_ADMIN]
        )


class GlenfieldBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.internal, 24)


class GlenfieldBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.internal, 24)


class DoncasterBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 13)


class DoncasterBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 13)


class SheffieldBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 14)


class SheffieldBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 14)


class KetteringBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 15)


class KetteringBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 15)


class ChesterfieldBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 16)


class ChesterfieldBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 16)


class GranthamBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 17)


class GranthamBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 17)


class LincolnBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 18)


class LincolnBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 18)


class NorthamptonBriccsRedcapBloodSamplesMissing(
        BriccsRedcapBloodSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 19)


class NorthamptonBriccsRedcapUrineSamplesMissing(
        BriccsRedcapUrineSamplesMissing):
    def __init__(self):
        super().__init__(RedcapInstance.external, 19)
