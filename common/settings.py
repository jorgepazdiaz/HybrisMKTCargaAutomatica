# -*- coding: utf-8 -*-
# INPUT SETTINGS
SOURCE_ENCODING = 'utf8'
SOURCE_DELIMITER = ','

# OUTPUT SETTINGS
# MODE = 'PRODUCTIVE'
MODE = 'TEST'
TEST_MAIL = 'brunoo.gonzalez+{}@gmail.com'
BATCH_SIZE = 4500
PREFIX_CONTACT = 'CONTACTS'
PREFIX_INTERACTION = 'INTERACTIONS'
PREFIX_CAMPANA_CONSULTORA = 'CAMPANAS_CONSULTORAS'
OUTPUT_FILE_TYPES = [PREFIX_CONTACT, PREFIX_INTERACTION, PREFIX_CAMPANA_CONSULTORA]

# PHONE VALIDATION
PHONE_REGEX = '^\+\d{11}$'

# EMAIL VALIDATION
LOCAL_PART_REGEX = '^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-/=?^_`''{|}~\.]+$'

# LOGGING
LOGGER_NAME = 'hybris_marketing_etl'
LOGGING_FILE = 'c:\Belcorp\logs\hybris_marketing_etl'
