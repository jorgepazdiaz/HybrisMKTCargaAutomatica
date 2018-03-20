import pyodbc
import requests
from requests.auth import HTTPBasicAuth
import time
import datetime
import json
from mapping.contacts import *
from mapping.interactions import *
from mapping.campanas_consultoras import *
from common.settings import LOGGER_NAME
import logging
from dal.conn_credentials import *
import re
import os


class SqlServerAccess:

    def __init__(self):
        self.conn = None
        self.logger = logging.getLogger('{}.dal.SqlServerAccess'.format(LOGGER_NAME))
        self.logger.debug('Initializing')

    def connect(self):
        self.logger.debug('Connecting to BD {} on server {}'.format(SQL_SERVER, SQL_DB))
        if self.conn is None:
            conn_string = 'Driver=' + SQL_DRIVER + ';' + \
                          'Server=' + SQL_SERVER + ';' + \
                          'Database =' + SQL_DB + ';' + \
                          'UID=' + SQL_UID + ';' + \
                          'PWD=' + SQL_PWD + ';' + \
                          'Trusted_Connection=' + SQL_TRUSTED
            self.conn = pyodbc.connect(conn_string)
        return self.conn

    def close(self):
        self.logger.debug('Disconnecting from BD {} on server {}'.format(SQL_SERVER, SQL_DB))
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def reconnect(self):
        self.close()
        return self.connect()


# Obtiene el timestamp actual y trunca la cantidad de caracteres, reemplazando el . que está de más
def get_timestamp_str():
    return '/Date({})/'.format(str(round(time.time(), 3)).replace('.', ''))


def get_timestamp_from_date_str(date_to_parse):
    result = str(time.mktime(datetime.datetime.strptime(date_to_parse, "%Y%m%d").timetuple())).replace('.', '00')
    return '/Date({})/'.format(result)


# Precondición: el contacto tiene todas los datos completos con las claves correctas
def transform_contacts(values, business_objects):
    to_import = []
    for row in values.values():
        to_odata = {}
        for key in ODATA_CONTACT_MAPPING:
            if key not in row.keys():
                raise Exception('Key {} not found'.format(key))
            elif key in [O_ID, O_CODIGOEBELISTA]:
                # Modificación de int a str
                to_odata[ODATA_CONTACT_MAPPING[key]] = str(row[key])
            elif key in [O_DATE_OF_BIRTH]:
                # Modificación de fecha
                to_odata[ODATA_CONTACT_MAPPING[key]] = get_timestamp_from_date_str(row[key])
            else:
                to_odata[ODATA_CONTACT_MAPPING[key]] = row[key]
        # Agregado de Timestamp para servicio
        to_odata['Timestamp'] = get_timestamp_str()
        if to_odata[ODATA_CONTACT_MAPPING[O_ID]] in business_objects[ODATA_INTERACTION]:
            facets = []
            for interaction in business_objects[ODATA_INTERACTION][to_odata[ODATA_CONTACT_MAPPING[O_ID]]]:
                # TODO: parametrizar atributos del facet
                facets.append({
                    'Id': interaction[O_ID],
                    'IdOrigin': interaction[O_ID_ORIGIN],
                    'Timestamp': get_timestamp_str()
                })
            to_odata['Facets'] = facets
        to_import.append(to_odata)
    return to_import


def transform_campanas_consultora(values):
    to_import = []
    for row in values.values():
        to_odata = {}
        for key in ODATA_CAMPANA_CONSULTORA_MAPPING:
            if key not in row.keys():
                raise Exception('Key {} not found'.format(key))
            else:
                if key in [O_ANIO_CAMPANA_EXPOSICION, O_NRO_CAMPANA_EXPOSICION, O_ANIO_CAMPANA_PROCESO,
                           O_NRO_CAMPANA_PROCESO, O_ANIO_CAMPANA_INGRESO, O_NRO_CAMPANA_INGRESO,
                           O_COD_COMPORTAMIENTO, O_COD_ZONA, O_EDAD_BELCORP, O_FLAG_CELULAR,
                           O_FLAG_CONSTANCIA_NUEVAS, O_FLAG_CORREO, O_FLAG_DEUDA, O_FLAG_INSCRITA,
                           O_FLAG_IP_UNICO, O_FLAG_OFERTA_DIGITAL_UC, O_FLAG_PASO_PEDIDO,
                           O_FLAG_PASO_PEDIDO_CACT, O_FLAG_TP1, O_FLAG_TP2, O_IP_UNICO_PU5C,
                           O_NRO_CAMPANA_NUEVAS, O_NRO_PEDIDOS_NUEVAS, O_OFERTA_DIGITAL_PU5C,
                           O_FLAG_INSCRITA_GANA_MAS]:
                    # Modificación de int a str
                    to_odata[ODATA_CAMPANA_CONSULTORA_MAPPING[key]] = str(row[key])
                elif key in [O_FECHA_ENVIO, O_FECHA_INICIO_FACTURACION, O_FECHA_FIN_FACTURACION,
                             O_FECHA_INICIO_VENTA, O_FECHA_FIN_VENTA]:
                    # Modificación de fecha
                    to_odata[ODATA_CAMPANA_CONSULTORA_MAPPING[key]] = '/Date({})/'.format(row[key])
                else:
                    to_odata[ODATA_CAMPANA_CONSULTORA_MAPPING[key]] = row[key]
        to_import.append(to_odata)
    return to_import


def transform_business_objects(business_objects):
    result = {}
    for bo, values in business_objects.items():
        if bo == ODATA_CONTACT:
            result[bo] = transform_contacts(values, business_objects)
        elif bo == ODATA_CAMPANA_CONSULTORA:
            result[bo] = transform_campanas_consultora(values)
        elif bo == ODATA_INTERACTION:
            # result[bo] = transform_interactions(values)
            pass
        # TODO: implementar cuando sea necesario
        elif bo == 'Interests':
            pass
        # TODO: implementar cuando sea necesario
        elif bo == 'Products':
            pass
        # TODO: implementar cuando sea necesario
        elif bo == 'ProductCategories':
            pass
        else:
            result[bo] = None
    return result


def generate_batch_json(values):
    json_batch = ''
    json_batch += '--batch' + os.linesep
    json_batch += 'content-type: multipart/mixed;boundary=changeset' + os.linesep

    for row in values:
        json_batch += os.linesep
        json_batch += '--changeset' + os.linesep
        json_batch += 'content-type: application/http' + os.linesep
        json_batch += 'content-transfer-encoding: binary' + os.linesep
        json_batch += os.linesep
        json_batch += 'POST YY1_CAMPANAS_CONSULTORA HTTP/1.1' + os.linesep
        json_batch += 'Accept: application/json' + os.linesep
        json_batch += 'content-type: application/json' + os.linesep
        json_batch += 'SAP-CUAN-ForceSynchronousProcessing: X' + os.linesep
        json_batch += os.linesep
        json_batch += json.dumps(row)
        json_batch += os.linesep
    json_batch += os.linesep
    json_batch += '--changeset--' + os.linesep
    json_batch += '--batch--'
    return json_batch


class ODataAccess:
    def __init__(self):
        self.logger = logging.getLogger('{}.dal.ODataAccess'.format(LOGGER_NAME))
        self.logger.debug('Initializing')
        self.session = None
        self.session_created_at = None
        self.csrf_token = None
        self.get_csrf_token()

    def get_csrf_token(self):
        self.logger.debug('Fetching CSRF token')
        headers = {
            'x-csrf-token': 'Fetch',
            'cache-control': 'no-cache'
        }
        self.session = requests.session()
        response = self.session.get(ODATA_BASE_URL + ODATA_GET_CSRF,
                                    headers=headers,
                                    auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD))
        if response.status_code == 200:
            self.logger.info('CSRF token fetched - {} {}'.format(response.status_code, response.reason))
            self.csrf_token = response.headers['x-csrf-token']
            self.session_created_at = datetime.datetime.now()
        else:
            self.logger.error('CSRF token error - {} {}'.format(response.status_code, response.reason))
            raise Exception('GET_CSRF_TOKEN - Status code: {}'.format(response.status_code))

    def logoff(self):
        self.logger.debug('Logging off')
        headers = {
            'x-csrf-token': self.csrf_token
        }
        self.session = requests.session()
        response = self.session.post(ODATA_LOGOFF_URL,
                                     headers=headers,
                                     auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD))
        if response.status_code == 200:
            self.logger.info('Logoff successful - {} {}'.format(response.status_code, response.reason))
        else:
            self.logger.error('Logoff error - {} {}'.format(response.status_code, response.reason))

    def post_data(self, business_objects):
        self.logger.debug('Posting data')
        new_bo = transform_business_objects(business_objects)
        for bo_name, bo_values in new_bo.items():
            # Se descartan las interacciones porque se suben en conjunto con los contactos
            if bo_name != ODATA_INTERACTION:
                last_index = 0
                batch_size = 1
                if bo_name == ODATA_CONTACT:
                    batch_size = ODATA_CONTACT_BATCH_SIZE
                elif bo_name == ODATA_CAMPANA_CONSULTORA:
                    batch_size = ODATA_CAMPANAS_CONSULTORA_BATCH_SIZE
                if bo_name in [ODATA_CONTACT, ODATA_INTERACTION]:
                    post_url = ODATA_BASE_URL + ODATA_POST_IMPORT_HEADERS
                elif bo_name == ODATA_CAMPANA_CONSULTORA:
                    post_url = ODATA_BASE_URL + ODATA_POST_CAMPANAS_CONSULTORA
                self.logger.debug('post_data - object[{}] batch_size[{}] post_url[{}]'.format(bo_name, batch_size,
                                                                                              post_url))
                while last_index < len(bo_values):
                    next_index = min(last_index + batch_size, len(bo_values))
                    self.logger.debug('post_data - processing {}[{}:{}]'.format(bo_name, last_index, next_index))
                    time.sleep(ODATA_IDLE_TIME)
                    if not self.session and self.session_created_at + datetime.timedelta(minutes=ODATA_SESSION_MAX_TTL) < \
                            datetime.datetime.now():
                        self.get_csrf_token()
                    headers = {
                        'x-csrf-token': self.csrf_token,
                        'content-type': 'application/json',
                        'cache-control': 'no-cache'
                    }
                    if bo_name == ODATA_CONTACT:
                        json_header = {
                            'Id': '',
                            'Timestamp': get_timestamp_str(),
                            'UserName': 'INTEGRATION',
                            'SourceSystemType': 'EXT',
                            'SourceSystemId': 'ODATA',
                            'ForceSynchronousProcessing': True
                        }
                        json_data = json_header
                        json_data[bo_name] = bo_values[last_index:next_index]
                        json_data = json.dumps(json_data)
                        post_url = ODATA_BASE_URL + ODATA_POST_IMPORT_HEADERS
                    elif bo_name == ODATA_CAMPANA_CONSULTORA:
                        headers['content-type'] = 'multipart/mixed;boundary=batch'
                        json_data = generate_batch_json(bo_values[last_index:next_index])
                        post_url = ODATA_BASE_URL + ODATA_POST_CAMPANAS_CONSULTORA_BATCH
                    self.logger.debug('post_data - sending POST {}[{}:{}]'.format(bo_name, last_index, next_index))
                    response = self.session.post(post_url,
                                                 headers=headers,
                                                 auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                                 data=json_data)

                    if bo_name == ODATA_CONTACT and response.status_code == 201:
                        self.logger.info('post_data - batch {}[{}:{}] successful - {} {}'.
                                         format(bo_name, last_index, next_index, response.status_code, response.reason))
                    elif bo_name == ODATA_CAMPANA_CONSULTORA and response.status_code == 202:
                        self.logger.debug('post_data - batch {}[{}:{}] finding 201 CREATED in response'.
                                          format(bo_name, last_index, next_index))
                        matches = re.search('HTTP/1.1 201 Created', str(response.content), re.IGNORECASE)
                        if not matches:
                            self.logger.debug('post_data - batch {}[{}:{}] finding duplicate key in response'.
                                               format(bo_name, last_index, next_index))
                            matches = re.search('Instance with the same key already exists', str(response.content),
                                                re.IGNORECASE)
                            if matches:
                                headers['content-type'] = 'application/json'
                                for i in range(last_index, next_index):
                                    item = bo_values[i]
                                    self.logger.debug("post_data - item {}[{}] getting SAP_UUID - {}='{}' and {}='{}'".
                                                      format(bo_name, i, O_IDORIGIN, item[O_IDORIGIN],
                                                             ODATA_CAMPANA_CONSULTORA_MAPPING[O_ID_CAMPANA_CONSULTORA],
                                                             item[ODATA_CAMPANA_CONSULTORA_MAPPING[O_ID_CAMPANA_CONSULTORA]]))
                                    get_url = ODATA_BASE_URL + ODATA_POST_CAMPANAS_CONSULTORA + "?$select=SAP_UUID&$filter=" + \
                                              O_IDORIGIN + " eq '" + item[O_IDORIGIN] + "' and " + \
                                              ODATA_CAMPANA_CONSULTORA_MAPPING[O_ID_CAMPANA_CONSULTORA] + " eq '" + \
                                              item[ODATA_CAMPANA_CONSULTORA_MAPPING[O_ID_CAMPANA_CONSULTORA]] + "'"
                                    response = self.session.get(get_url,
                                                                headers=headers,
                                                                auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD))
                                    if response.status_code == 200:
                                        self.logger.debug("post_data - item {}[{}] finding SAP_UUID in response".
                                                          format(bo_name, i))
                                        matches = re.search('<d:SAP_UUID>(.*?)</d:SAP_UUID>', str(response.content),
                                                            re.IGNORECASE)
                                        if matches:
                                            sap_uuid = matches.group(1)
                                            put_url = ODATA_BASE_URL + ODATA_POST_CAMPANAS_CONSULTORA + "(guid'" + \
                                                      sap_uuid + "')"
                                            self.logger.debug("post_data - item {}[{}] sending PUT - SAP_UUID='{}'".
                                                              format(bo_name, i, sap_uuid))
                                            response = self.session.put(put_url,
                                                                        headers=headers,
                                                                        auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                                                        data=json.dumps(item))
                                            if response.status_code == 204:
                                                self.logger.info('post_data - item {}[{}] PUT successful - {} {}'.
                                                                 format(bo_name, i, response.status_code,
                                                                        response.reason))
                                            else:
                                                self.logger.error('post_data - item {}[{}] PUT error - {} {}'.
                                                                  format(bo_name, i, response.status_code,
                                                                         response.reason))
                                        else:
                                            self.logger.error('post_data - item {}[{}] SAP_UUID not found'.
                                                              format(bo_name, i))
                                    else:
                                        self.logger.error('post_data - item {}[{}] SAP_UUID error - {} {}'.
                                                          format(bo_name, i, response.status_code, response.reason))
                            else:
                                self.logger.error('post_data - batch {}[{}:{}] unexpected message in response - {} {}: {}'.
                                                  format(bo_name, last_index, next_index, response.status_code,
                                                         response.reason, response.content))
                        else:
                            self.logger.info('post_data - batch {}[{}:{}] successful - {} {}'.
                                             format(bo_name, last_index, next_index, response.status_code,
                                                    response.reason))
                    else:
                        self.logger.error('post_data - batch {}[{}:{}] error - {} {}'.
                                          format(bo_name, last_index, next_index, response.status_code, response.reason))
                    last_index += batch_size
        self.logoff()
        self.logger.debug('Posting data completed')
