# -*- coding: utf-8 -*-
# Database
SQL_DRIVER = "{SQL Server Native Client 11.0}"
SQL_SERVER = ""
SQL_DB = "BelcorpCostaRica"
SQL_UID = "belcorp"
SQL_PWD = "belcorp"
SQL_TRUSTED = "yes"

# OData Service
ODATA_BASE_URL = "https://my300972-api.s4hana.ondemand.com/sap/opu/odata/sap/"
ODATA_GET_CSRF = "CUAN_IMPORT_SRV/$metadata"
ODATA_LOGOFF = "public/bc/icf/logoff"
ODATA_POST_CONTACT = "CUAN_IMPORT_SRV/ImportHeaders"
ODATA_POST_CAMPANA_CONSULTORA = "YY1_CAMPANAS_CONSULTORA_CDS/YY1_CAMPANAS_CONSULTORA"
ODATA_USER = "INTEGRATION"
ODATA_PASSWORD = "bGJZww]cfz9mFimjjhifvoVKYidmSRdMJFiuYKFk"
ODATA_SESSION_MAX_TTL = 30 # Minutes
ODATA_BATCH_SIZE = 500

# Constants
ODATA_CONTACT = 'Contacts'
ODATA_CAMPANA_CONSULTORA = 'CampanaConsultora'