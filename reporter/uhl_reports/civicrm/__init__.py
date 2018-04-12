def get_case_link(link_text, case_id, contact_id):
    CIVICRM_CASE_URL = ('[{}]('
                        'http://lcbru.xuhl-tr.nhs.uk/civicrm/contact/view/case'
                        '?id={}&cid={}&action=view)')

    return (CIVICRM_CASE_URL.format(
        link_text,
        case_id,
        contact_id))


def get_contact_link(link_text, contact_id):
    CIVICRM_CONTACT_URL = (
        '[{}]('
        'http://lcbru.xuhl-tr.nhs.uk/civicrm/contact/view'
        '?cid={})')

    return (CIVICRM_CONTACT_URL.format(
        link_text,
        contact_id))


def get_contact_id_search_link(link_text, contact_id):
    CIVICRM_SEARCH_URL = (
        '[{}]('
        'http://lcbru.xuhl-tr.nhs.uk/content/participant_search/{})')

    return (CIVICRM_SEARCH_URL.format(
        link_text,
        contact_id))
