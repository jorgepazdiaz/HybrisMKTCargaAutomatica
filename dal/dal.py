import pyodbc
import requests
from requests.auth import HTTPBasicAuth
import time
import datetime
import json
from mapping.contacts import *
from mapping.campanas_consultoras import *
from dal.conn_credentials import *
import re


class SqlServerAccess:

    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None:
            conn_string = "Driver=" + SQL_DRIVER + ";" + \
                          "Server=" + SQL_SERVER + ";" + \
                          "Database =" + SQL_DB + ";" + \
                          "UID=" + SQL_UID + ";" + \
                          "PWD=" + SQL_PWD + ";" + \
                          "Trusted_Connection=" + SQL_TRUSTED
            self.conn = pyodbc.connect(conn_string)
        return self.conn

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def reconnect(self):
        self.close()
        return self.connect()


# Obtiene el timestamp actual y trunca la cantidad de caracteres, reemplazando el . que está de más
def get_timestamp_str():
    return "/Date({})/".format(str(round(time.time(), 3)).replace(".", ""))


def transform_contacts(values):
    to_import = []
    for row in values.values():
        to_odata = {}
        for key in ODATA_CONTACT_MAPPING:
            if key not in row.keys():
                raise Exception('ODATA - Key {} not found'.format(key))
            else:
                if key in [O_ID, O_CODIGOEBELISTA]:
                    # Modificación de int a str
                    to_odata[ODATA_CONTACT_MAPPING[key]] = str(row[key])
                elif key in [O_DATE_OF_BIRTH]:
                    # Modificación de fecha
                    to_odata[ODATA_CONTACT_MAPPING[key]] = '/Date({})/'.format(row[key])
                else:
                    to_odata[ODATA_CONTACT_MAPPING[key]] = row[key]
        # Agregado de Timestamp para servicio
        to_odata['Timestamp'] = get_timestamp_str()
        to_import.append(to_odata)
    return to_import


def transform_campanas_consultora(values):
    to_import = []
    for row in values.values():
        to_odata = {}
        for key in ODATA_CAMPANA_CONSULTORA_MAPPING:
            if key not in row.keys():
                raise Exception('ODATA - Key {} not found'.format(key))
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
                    # to_odata[ODATA_CAMPANA_CONSULTORA_MAPPING[key]] = ''
                else:
                    to_odata[ODATA_CAMPANA_CONSULTORA_MAPPING[key]] = row[key]
        to_import.append(to_odata)
    return to_import


# TODO: implementar
def transform_interactions(values):
    return 1


def transform_business_objects(business_objects):
    result = {}
    for bo, values in business_objects.items():
        if bo == ODATA_CONTACT:
            result[bo] = transform_contacts(values)
        elif bo == ODATA_CAMPANA_CONSULTORA:
            result[bo] = transform_campanas_consultora(values)
        elif bo == "Interactions":
            result[bo] = transform_interactions(values)
        # TODO: implementar cuando sea necesario
        elif bo == "Interests":
            pass
        # TODO: implementar cuando sea necesario
        elif bo == "Products":
            pass
        # TODO: implementar cuando sea necesario
        elif bo == "ProductCategories":
            pass
        else:
            result[bo] = None
    return result


class ODataAccess:
    def __init__(self):
        self.session = None
        self.session_created_at = None
        self.csrf_token = None
        self.get_csrf_token()

    def get_csrf_token(self):
        headers = {
            "x-csrf-token": "Fetch",
            "cache-control": "no-cache"
        }
        self.session = requests.session()
        response = self.session.get(ODATA_BASE_URL + ODATA_GET_CSRF,
                                    headers=headers,
                                    auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD))
        if response.status_code == 200:
            self.csrf_token = response.headers["x-csrf-token"]
            self.session_created_at = datetime.datetime.now()
        else:
            # TODO: unificar retorno de resultados y errores. raise Exception
            raise Exception('GET_CSRF_TOKEN - Status code:{}'.format(response.status_code))

    def post_data(self, business_objects):
        # Invocación de servicio de Business Objects
        print("ODATA - Invoke service")
        json_header = {
            "Id": "",
            "Timestamp": get_timestamp_str(),
            "UserName": "INTEGRATION",
            "SourceSystemType": "EXT",
            "SourceSystemId": "ODATA"
        }
        new_bo = transform_business_objects(business_objects)
        # Invocación de servicio en batch: se separa por entidad para tener mayor control de errores
        for bo_name, bo_values in new_bo.items():
            print("ODATA - {}: Sending posts".format(bo_name))
            last_index = 0
            batch_size = 1
            if bo_name == ODATA_CONTACT:
                batch_size = ODATA_BATCH_SIZE
            while last_index < len(bo_values):
                # If no session or TTL expired get new CSRF-TOKEN
                if not self.session or self.session_created_at + datetime.timedelta(minutes=ODATA_SESSION_MAX_TTL) < \
                        datetime.datetime.now():
                    print("ODATA - {}: Getting new CSRF-TOKEN".format(bo_name))
                    self.get_csrf_token()
                headers = {
                    "x-csrf-token": self.csrf_token,
                    "content-type": "application/json",
                    "cache-control": "no-cache"
                }

                if bo_name == ODATA_CONTACT:
                    json_data = json_header
                    json_data[bo_name] = bo_values[last_index:last_index + batch_size]
                    post_url = ODATA_BASE_URL + ODATA_POST_CONTACT
                elif bo_name == ODATA_CAMPANA_CONSULTORA:
                    json_data = bo_values[last_index]
                    post_url = ODATA_BASE_URL + ODATA_POST_CAMPANA_CONSULTORA

                response = self.session.post(post_url,
                                             headers=headers,
                                             auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                             data=json.dumps(json_data))

                if response.status_code == 201:
                    print("ODATA - {}[OK]: Status code: {}. Index from {} to {}".format(bo_name, response.status_code,
                                                                                        last_index, last_index +
                                                                                        batch_size))
                elif bo_name == ODATA_CAMPANA_CONSULTORA and response.status_code == 400:
                    print("ODATA - {}: Getting SAP_UUID - {}='{}' and {}='{}'".format(bo_name, O_IDORIGIN,
                                                                                      json_data[O_IDORIGIN],
                                                                                      ODATA_CAMPANA_CONSULTORA_MAPPING[
                                                                                          O_ID_CAMPANA_CONSULTORA],
                                                                                      json_data[
                                                                                          ODATA_CAMPANA_CONSULTORA_MAPPING[
                                                                                              O_ID_CAMPANA_CONSULTORA]]))
                    get_url = ODATA_BASE_URL + ODATA_POST_CAMPANA_CONSULTORA + "?$select=SAP_UUID&$filter=" + \
                              O_IDORIGIN + " eq '" + json_data[O_IDORIGIN] + "' and " + \
                              ODATA_CAMPANA_CONSULTORA_MAPPING[O_ID_CAMPANA_CONSULTORA] + " eq '" + \
                              json_data[ODATA_CAMPANA_CONSULTORA_MAPPING[O_ID_CAMPANA_CONSULTORA]] + "'"
                    # get_url = "https://my300972-api.s4hana.ondemand.com/sap/opu/odata/sap/YY1_CAMPANAS_CONSULTORA_CDS/YY1_CAMPANAS_CONSULTORA?$select=SAP_UUID&$filter=ID_ORIGIN eq 'SAP_ODATA_IMPORT' and IdCampanaConsultora eq '201806_2222_UY'"
                    response = self.session.get(get_url,
                                                headers=headers,
                                                auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD))
                    if response.status_code == 200:
                        matches = re.search('<d:SAP_UUID>(.*?)</d:SAP_UUID>', str(response.content), re.IGNORECASE)
                        if matches:
                            sap_uuid = matches.group(1)
                            put_url = ODATA_BASE_URL + ODATA_POST_CAMPANA_CONSULTORA + "(guid'" + sap_uuid + "')"
                            response = self.session.put(put_url,
                                                        headers=headers,
                                                        auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                                        data=json.dumps(json_data))
                            if response.status_code == 204:
                                print("ODATA - {}[OK]: Status code: {}. Index from {} to {}".format(bo_name,
                                                                                                    response.status_code,
                                                                                                    last_index,
                                                                                                    last_index +
                                                                                                    batch_size))
                            else:
                                print("ODATA - {}[ERROR]: Status code: {}. Index from {} to {}".format(bo_name,
                                                                                                       response.status_code,
                                                                                                       last_index,
                                                                                                       last_index +
                                                                                                       batch_size))
                        else:
                            print("ODATA - {}[ERROR]: No SAP_UUID found. Index from {} to {}".format(bo_name,
                                                                                                     last_index,
                                                                                                     last_index +
                                                                                                     batch_size))
                    else:
                        print("ODATA - {}[ERROR]: Status code: {}. Index from {} to {}".format(bo_name,
                                                                                               response.status_code,
                                                                                               last_index,
                                                                                               last_index +
                                                                                               batch_size))
                else:
                    print("ODATA - {}[ERROR]: Status code: {}. Index from {} to {}".format(bo_name, response.status_code,
                                                                                           last_index, last_index +
                                                                                           batch_size))
                last_index += batch_size
            print("ODATA - {}: Finished".format(bo_name))
            # TODO: logoff sap/public/bc/icf/logoff
        print(new_bo)
