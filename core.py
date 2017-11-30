import logging
from collections import OrderedDict
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse

log = logging.getLogger("kms_qr")

BASE_URL = "http://kmsuj.im.uj.edu.pl/member/"


def gen_data(name, surname, kms, album, wmii, url=BASE_URL, **kwargs):
    parameters = OrderedDict([
        ("name", name),
        ("surname", surname),
        ("kms", kms),
        ("album", album),
        ("wmii", wmii),
    ])
    query = urlencode(parameters)

    url_parts = list(urlparse(url))
    url_parts[4] = query
    result = urlunparse(url_parts)
    return result
