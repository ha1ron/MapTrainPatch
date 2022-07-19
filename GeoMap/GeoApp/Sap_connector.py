import json
import requests
from requests.auth import HTTPBasicAuth
from .local_settings import sap_opt



def sapCreateSession():  # Создание сессии для запросов oDATA

    # Конектимся к SAP

    session = requests.Session()
    session.headers.update({'Connection': 'keep-alive', 'X-CSRF-TOKEN': 'Fetch'})
    try:
        r = session.get(sap_opt['baseurl'], auth=(sap_opt['user'], sap_opt['passwd']), verify=sap_opt['verify'])
    except:
        message = "Нет соединения с системой %s  %s" % (sap_opt['mandt'], sap_opt['name'])
        return ('NO TOKEN', 'NoSession', message)
    token = r.headers['x-csrf-token']
    sess = (token, session, None)
    return sess


def get_oData_set(set, filter, format='$format=json'):
    session = sapCreateSession()  # Создаю сессию
    token = session[0]
    ss = session[1]
    url = sap_opt['baseurl'] + set + '?' + filter + '&' + format
    headers = {'Content-type': 'application/json;charset=utf-8',
               'X-CSRF-TOKEN': token}  # обновляем хидер и добавляем токен
    auth = HTTPBasicAuth(sap_opt['user'], sap_opt['passwd'])  # для auth
    get = ss.get(url, headers=headers, auth=auth, verify=sap_opt['verify'])  # Запрос данных
    jdata = json.loads(get.text)
    if jdata and 'error' not in jdata:
        jdata = jdata.get('d').get('results')
    else:
        jdata = ''
    return jdata
