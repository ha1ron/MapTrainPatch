import requests
from requests.auth import HTTPBasicAuth
import json
from .local_settings import server_url


def get_set(set, filter):
    s = requests.Session()
    s.headers.update({'Connection': 'keep-alive', 'X-CSRF-TOKEN': 'Fetch'})
    url = server_url + set + filter
    r = s.get(url, auth=HTTPBasicAuth('ocrv', 'ocrv'))
    return json.loads(r.text)

# aa = get_set('StNumberingSet', '?MONTH=202112&poezd=0054055945001035')


