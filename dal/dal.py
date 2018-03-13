import pyodbc
import requests
from requests.auth import HTTPBasicAuth
import time
import datetime
import json
from mapping.contacts import *
from dal.conn_credentials import *


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

    def close(self, driver, server, db, uid, pwd, trusted):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def reconnect(self, driver, server, db, uid, pwd, trusted):
        self.close()
        return self.connect()


# Obtiene el timestamp actual y trunca la cantidad de caracteres, reemplazando el . que está de más
def get_timestamp_str():
    return "/Date({})/".format(str(round(time.time(), 3)).replace(".", ""))


def transform_contacts(values):
    to_import = []
    for contact in values.values():
        contact_odata = {}
        for key in ODATA_CONTACT_MAPPING:
            if key not in contact.keys():
                raise Exception('ODATA - Key {} not found'.format(key))
            else:
                if key in [O_ID, O_CODIGOEBELISTA]:
                    # Modificación de int a str
                    contact_odata[ODATA_CONTACT_MAPPING[key]] = str(contact[key])
                elif key in [O_DATE_OF_BIRTH]:
                    # Modificación de fecha
                    contact_odata[ODATA_CONTACT_MAPPING[key]] = '/Date({})/'.format(contact[key])
                else:
                    contact_odata[ODATA_CONTACT_MAPPING[key]] = contact[key]
        # Agregado de Timestamp para servicio
        contact_odata['Timestamp'] = get_timestamp_str()
        to_import.append(contact_odata)
    # TODO: Handle discardes contacts
    return to_import


# TODO: implementar
def transform_campanas_consultora(values):
    return 1


# TODO: implementar
def transform_interactions(values):
    return 1


def transform_business_objects(business_objects):
    result = {}
    for bo, values in business_objects.items():
        if bo == "Contacts":
            result[bo] = transform_contacts(values)
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


def transform_custom_business_objects(custom_business_objects):
    result = {}
    for bo, values in custom_business_objects.items():
        if bo == "CampanasConsultora":
            result[bo] = transform_campanas_consultora(values)
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

    def post_data(self, business_objects, custom_business_objects):
        # Invocación de servicio de Business Objects
        print("ODATA - Invoke service for Business Objects")
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
            last_index = 0
            print("ODATA - {}: Sending posts".format(bo_name))
            while last_index < len(bo_values):
                # If no session or TTL expired get new CSRF-TOKEN
                if self.session and self.session_created_at + datetime.timedelta(minutes=SESSION_MAX_TTL_MINUTES) < \
                        datetime.datetime.now():
                    print("ODATA - {}: Getting new CSRF-TOKEN".format(bo_name))
                    self.get_csrf_token()
                headers = {
                    "x-csrf-token": self.csrf_token,
                    "content-type": "application/json",
                    "cache-control": "no-cache"
                }
                json_data = json_header
                json_data[bo_name] = bo_values[last_index:last_index + ODATA_BATCH_SIZE]
                if bo_name == 'Contacts':
                    post_url = ODATA_BASE_URL + ODATA_POST_IMPORT_HEADERS
                # TODO: set CBO URL
                elif bo_name == 'Campanas Consultora':
                    post_url = ODATA_BASE_URL + ODATA_POST_CAMPANAS_CONSULTORA
                response = self.session.post(post_url,
                                             headers=headers,
                                             auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                             data=json.dumps(json_data))
                if response.status_code == 201:
                    print("ODATA - {}[OK]: Status code: {}. Index from {} to {}".format(bo_name, 201, last_index, last_index + ODATA_BATCH_SIZE))
                else:
                    print("ODATA - {}[ERROR]: Status code: {}. Index from {} to {}".format(bo_name, response.status_code, last_index, last_index + ODATA_BATCH_SIZE))
                last_index += ODATA_BATCH_SIZE
            # TODO: logoff sap/public/bc/icf/logoff
            # TODO: Invocación de servicio de Custom Business Objects
            # print("ODATA - Invoke service for Custom Business Objects")
            # new_cbo = transform_custom_business_objects(custom_business_objects)
