# -*- coding: utf-8 -*-
# Database
SQL_DRIVER = '{SQL Server Native Client 11.0}'
SQL_SERVER = ''
SQL_DB = 'BelcorpCostaRica'
SQL_UID = 'belcorp'
SQL_PWD = 'belcorp'
SQL_TRUSTED = 'yes'

# OData Service
ODATA_BASE_URL = 'https://my300972-api.s4hana.ondemand.com/sap/opu/odata/sap/'
ODATA_GET_CSRF = 'CUAN_IMPORT_SRV/$metadata'
ODATA_LOGOFF_URL = 'https://my300972-api.s4hana.ondemand.com/sap/public/bc/icf/logoff'
ODATA_POST_IMPORT_HEADERS = 'CUAN_IMPORT_SRV/ImportHeaders'
ODATA_POST_CAMPANAS_CONSULTORA_BATCH = 'YY1_CAMPANAS_CONSULTORA_CDS/$batch'
ODATA_POST_CAMPANAS_CONSULTORA = 'YY1_CAMPANAS_CONSULTORA_CDS/YY1_CAMPANAS_CONSULTORA'
ODATA_USER = 'INTEGRATION'
ODATA_PASSWORD = 'bGJZww]cfz9mFimjjhifvoVKYidmSRdMJFiuYKFk'
ODATA_SESSION_MAX_TTL = 30 # Minutes
ODATA_IDLE_TIME = 2 # Seconds
ODATA_CONTACT_BATCH_SIZE = 500
ODATA_CAMPANAS_CONSULTORA_BATCH_SIZE = 100

# Constants
ODATA_CONTACT = 'Contacts'
ODATA_INTERACTION = 'Interactions'
ODATA_CAMPANA_CONSULTORA = 'CampanaConsultora'
