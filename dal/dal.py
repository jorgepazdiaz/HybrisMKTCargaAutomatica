from dal.conn_credentials import *
import pyodbc
import requests
from requests.auth import HTTPBasicAuth
import time
import datetime
import json
from mapping.contacts import CONTACT_FIELDS
import mapping.contacts


class SqlServerAccess:

    def __init__(self):
        self.conn = None

    # def connect(self, driver, server, db, uid, pwd, trusted):
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
    result = []
    for contact in values.values():
        # Copia de diccionario de contacto y edición de claves
        contact_odata = contact.copy()
        for contact_field in CONTACT_FIELDS:
            # Si existe la clave destino: cambio de nombre de clave
            try:
                # Chequea que tenga un valor diferente de vacío
                if contact_odata[getattr(mapping.contacts, 'O_{}'.format(contact_field))] != '':
                    value = contact_odata.pop(getattr(mapping.contacts, 'O_{}'.format(contact_field)))
                    # Modificaciones a atributos por cambio de tipo de dato
                    if contact_field in ['ID', 'CODIGOEBELISTA']:
                        # Modificación de int a str
                        value = str(value)
                    elif contact_field in ['DATE_OF_BIRTH']:
                        # Modificación de fecha
                        value = '/Date({})/'.format(value)
                    contact_odata[getattr(mapping.contacts, 'S_{}'.format(contact_field))] = value
                else:
                    del contact_odata[getattr(mapping.contacts, 'O_{}'.format(contact_field))]
            except:
                # Si no existe la clave destino: elimino clave y valor de origen
                try:
                    del contact_odata[getattr(mapping.contacts, 'O_{}'.format(contact_field))]
                except:
                    pass
        # Agregado de Timestamp para servicio
        contact_odata['Timestamp'] = get_timestamp_str()
        result.append(contact_odata)
    return result


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
        elif bo == "Products":
            pass
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
        # TODO: unificar retorno de resultados y errores. raise Exception
        print("GET_CSRF_TOKEN - Status code:{}".format(response.status_code))
        return 1

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
            print("Resultado para {}".format(bo_name))
            while last_index < len(bo_values):
                # Verifica que esté dentro del TTL de la sesión
                if self.session and self.session_created_at + datetime.timedelta(minutes=SESSION_MAX_TTL_MINUTES) < \
                        datetime.datetime.now():
                    # TODO: verificar que el resultado fue ok, sino abortar
                    self.get_csrf_token()
                headers = {
                    "x-csrf-token": self.csrf_token,
                    "content-type": "application/json",
                    "cache-control": "no-cache"
                }
                json_data = json_header
                json_data[bo_name] = bo_values[last_index:last_index + ODATA_BATCH_SIZE]
                response = self.session.post(ODATA_BASE_URL + ODATA_POST_IMPORT_HEADERS,
                                             headers=headers,
                                             auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                             data=json.dumps(json_data))
                if response.status_code == 201:
                    print("POST_ODATA - Status code: {}. Index from {} to {}".format(201, last_index, last_index + ODATA_BATCH_SIZE))
                else:
                    print("POST_ODATA - Status code: {}. Index from {} to {}".format(response.status_code, last_index, last_index + ODATA_BATCH_SIZE))
                last_index += ODATA_BATCH_SIZE
            # TODO: Invocación de servicio de Custom Business Objects
            # print("ODATA - Invoke service for Custom Business Objects")
            # new_cbo = transform_custom_business_objects(custom_business_objects)
