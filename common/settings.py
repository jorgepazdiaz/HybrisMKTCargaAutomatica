# -*- coding: utf-8 -*-
# INPUT SETTINGS
SOURCE_ENCODING = 'utf8'
SOURCE_DELIMITER = ','

# OUTPUT SETTINGS
TEST_MAIL = 'brunoo.gonzalez+{}@gmail.com'
BATCH_SIZE = 4500
OUTPUT_CONTACTS_FOLDER = 'contacts'
OUTPUT_INTERACTIONS_FOLDER = 'interactions'
OUTPUT_CAMPANAS_CONSULTORAS_FOLDER = 'campanas_consultoras'
OUTPUT_SUBSCRIPTIONS_FOLDER = 'subscriptions'
PREFIX_CONTACT = 'CONTACTS'
PREFIX_INTERACTION = 'INTERACTIONS'
PREFIX_CAMPANA_CONSULTORA = 'CAMPANAS_CONSULTORAS'
PREFIX_SUBSCRIPTIONS = 'SUBSCRIPTIONS'
PREFIX_NEVERBOUNCE_EMAILS = 'NEVERBOUNCE_CACHE'
OUTPUT_FILE_TYPES = [PREFIX_CONTACT, PREFIX_INTERACTION, PREFIX_CAMPANA_CONSULTORA, PREFIX_NEVERBOUNCE_EMAILS, PREFIX_SUBSCRIPTIONS]

# NEVERBOUNCE
NB_VALID_RESULTS = ['valid']
NB_CSV_CACHE_FILE = 'C:\\Users\\rafael.torrado\\GIT\\PythonEnvs\\CargaAutomatica\\csv\\neverbounce\\neverbounce_cache_file.csv'
#NB_API_KEY = 'secret_081411c124998a20c9077f74fc549e4a'  # Pyxis'
NB_API_KEY = 'secret_ab8cde56d0d8e8eb1403d311d59f12ac' # Belcorp's
NB_EMAIL_KEY = 'email'
NB_SLEEP_SECONDS = 0.1
NB_SOURCE_DELIMITER = ';'
NB_DATA_SIZE = 200
# List of attributes that the input file must include
NB_EMAIL_ADDRESS = 'Dirección de Email'
NB_VALIDATION_RESULT = 'Resultado Validación'
NB_CONTACT_ID = 'Código Consultora'
NB_COUNTRY_ID = 'País'
NB_CACHE_FIELDS = [NB_CONTACT_ID, NB_COUNTRY_ID, NB_EMAIL_ADDRESS, NB_VALIDATION_RESULT]

# PHONE VALIDATION
#PHONE_REGEX = '^\+\d{11,12}$'
PHONE_REGEX = '^\+(\d{10}|\d{11}|\d{12}|\d{13}|\d{14})$'

# EMAIL VALIDATION
LOCAL_PART_REGEX = '^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-/=?^_`''{|}~\.]+$'

# LOGGING
LOGGER_NAME = 'hybris_marketing_etl'
