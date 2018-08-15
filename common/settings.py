# -*- coding: utf-8 -*-
# INPUT SETTINGS
SOURCE_ENCODING = 'utf8'
SOURCE_DELIMITER = ','

# OUTPUT SETTINGS
TEST_MAIL = 'brunoo.gonzalez+{}@gmail.com'
BATCH_SIZE = 4500
PREFIX_CONTACT = 'CONTACTS'
PREFIX_INTERACTION = 'INTERACTIONS'
PREFIX_CAMPANA_CONSULTORA = 'CAMPANAS_CONSULTORAS'
OUTPUT_FILE_TYPES = [PREFIX_CONTACT, PREFIX_INTERACTION, PREFIX_CAMPANA_CONSULTORA]

# NEVERBOUNCE
NB_INVALID_RESULTS = ['invalid', 'disposable', 'unknown', 'catchall', 'duplicate', 'bad_syntax']
NB_VALIDATION_RESULT_KEY = 'ValidationResult'
NB_CSV_CACHE_FILE = 'C:\\Users\\rafael.torrado\\GIT\\PythonEnvs\\CargaAutomatica\\csv\\neverbounce\\neverbounce_cache_file.csv'
NB_API_KEY = 'secret_081411c124998a20c9077f74fc549e4a'
NB_EMAIL_KEY = 'email'
#NB_SLEEP_SECONDS = 1
# List of attributes that the input file must include
NB_EMAIL_ADDRESS = 'EmailAddress'
NB_VALIDATION_RESULT = 'ValidationResult'
NB_CACHE_FIELDS = [NB_EMAIL_ADDRESS, NB_VALIDATION_RESULT]
PREFIX_NEVERBOUNCE_EMAILS = 'NEVERBOUNCE_EMAILS'

# PHONE VALIDATION
#PHONE_REGEX = '^\+\d{11,12}$'
PHONE_REGEX = '^\+(\d{10}|\d{11}|\d{12}|\d{13}|\d{14})$'

# EMAIL VALIDATION
LOCAL_PART_REGEX = '^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-/=?^_`''{|}~\.]+$'

# LOGGING
LOGGER_NAME = 'hybris_marketing_etl'
