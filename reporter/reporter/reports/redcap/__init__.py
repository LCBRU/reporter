from os.path import dirname, basename, isfile
import glob

modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]


BASE_URL_INTERNAL = "https://briccs.xuhl-tr.nhs.uk/redcap/redcap_v7.2.2/"
BASE_URL_EXTERNAL = "https://uhlbriccsext01.xuhl-tr.nhs.uk/redcap/redcap_v7.2.2/"


def get_redcap_link(link_text, project_id, record):
    REDCAP_RECORD_URL = (
        '[{}]({}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        BASE_URL_INTERNAL,
        project_id,
        record))


def get_redcap_external_link(link_text, project_id, record):
    REDCAP_RECORD_URL = (
        '[{}]({}/DataEntry/record_home.php'
        '?pid={}&id={})')

    return (REDCAP_RECORD_URL.format(
        link_text,
        BASE_URL_EXTERNAL,
        project_id,
        record))
