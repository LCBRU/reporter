from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]


def get_redcap_link(link_text, project_id, record):
    REDCAP_VERSION = 'v7.2.2'
    REDCAP_RECORD_URL = (
        '[{}](https://briccs.xuhl-tr.nhs.uk/redcap/'
        'redcap_{}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_VERSION,
        project_id,
        record))


def get_redcap_external_link(link_text, project_id, record):
    REDCAP_VERSION = 'v7.2.2'
    REDCAP_RECORD_URL = (
        '[{}](https://uhlbriccsext01.xuhl-tr.nhs.uk/redcap/'
        'redcap_{}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        REDCAP_VERSION,
        project_id,
        record))
