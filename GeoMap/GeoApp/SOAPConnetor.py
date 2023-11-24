from suds.client import Client
from bs4 import BeautifulSoup as bs
import json
from .local_settings import SOAP_opt
try:
    client = Client(SOAP_opt['wsdl'], username=SOAP_opt['user'], password=SOAP_opt['passwd'], retxml=True)
except:
    pass
# client = Client('http://saphanal.msk.oao.rzd:8000/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/z00_rgp_extr_uni3/200/z00_rgp_extr_uni3/z00_rgp_extr_uni3?sap-client=200',
#                 username='STADNIKOV', password='d9u6k3e2', retxml=True)


def getPoezdData(month, poezd):
    items = [appendSelParamValue('MONTH', 'I', 'EQ', month),
             appendSelParamValue('POEZD', 'I', 'EQ', poezd)]
    att_where_t = client.factory.create('Z00_DYN_WHERE_T')
    att_where_t.item = items
    response = client.service.Z00_RGP_EXTR_UNI3(IT_WHERE=att_where_t, I_OUT_FORMAT='JSON', I_SEL_DT='TD', I_SEL_ID='M2')
    xml = bs(response, 'xml')
    json_text = xml.find('RVAL').text
    json_response = json.loads(json_text).get('M2')[0]

    stantions = json.loads(json_response['st_edges'])
    coordinates = json.loads(json_response['st_coordinates'])
    start_end = json.loads(json_response['sf_data'])
    return stantions, coordinates, start_end


def getUnoData(month, uno, iddos):
    items = [appendSelParamValue('MONTH', 'I', 'EQ', month),
             appendSelParamValue('UNO', 'I', 'EQ', uno),
             appendSelParamValue('IDDOS', 'I', 'EQ', iddos)]
    att_where_t = client.factory.create('Z00_DYN_WHERE_T')
    att_where_t.item = items
    response = client.service.Z00_RGP_EXTR_UNI3(IT_WHERE=att_where_t, I_OUT_FORMAT='JSON', I_SEL_DT='TD', I_SEL_ID='M1')
    xml = bs(response, 'xml')
    json_text = xml.find('RVAL').text
    json_response = json.loads(json_text).get('M1')[0]
    stantions = json.loads(json_response['coordinate_full_list'])
    start_end_info = json.loads(json_response['start_end_info'])
    stantions_path_list = json.loads(json_response['stantions_path_list'])
    uno_path_list = json.loads(json_response['uno_path_list'])
    coordinates_uno_list = json.loads(json_response['coordinates_uno_list'])

    return stantions, start_end_info, stantions_path_list, uno_path_list, coordinates_uno_list


    # stantions = json.loads(json_response['st_edges'])
    # coordinates = json.loads(json_response['st_coordinates'])
    # start_end = json.loads(json_response['sf_data'])
    # return stantions, coordinates, start_end


def appendSelParamValue(fieldnm, sign, opt, low, high=''):
    option = client.factory.create('Z00_DYN_WHERE_S')

    option.FIELDNM = fieldnm
    option.SIGN = sign
    option.OPT = opt
    option.LOW = low
    option.HIGH = high
    return option


# getUnoData('202207', '001289278639', '0000000000')
