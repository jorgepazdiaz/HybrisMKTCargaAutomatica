# -*- coding: utf-8 -*-
# INPUT SETTINGS
SOURCE_FOLDER = '/Users/bruno/Downloads/IDATHA/Belcorp/ETL'
SOURCE_FILE = 'BelcorpCostaRica_InPut_HM_20180309.csv'
SOURCE_ENCODING = 'utf8'
SOURCE_DELIMITER = ','
OUTPUT_FOLDER = '/Users/bruno/Downloads/IDATHA/Belcorp/ETL/out'

# OUTPUT SETTINGS
MODE = 'PRODUCTIVE'
# MODE = 'TEST'
BATCH_SIZE = 4500
PREFIX_CONTACT = 'CONTACTS'
PREFIX_APP_INSTALLED = 'APP_TOKEN_INTERACTIONS'
PREFIX_CAMPANAS_CONSULTORA = 'CBO_CAMPANAS_CONSULTORA'
OUTPUT_FILE_TYPES = [PREFIX_CONTACT, PREFIX_APP_INSTALLED, PREFIX_CAMPANAS_CONSULTORA]

# PHONE VALIDATION
PHONE_REGEX = '^\+\d{11}$'

# EMAIL VALIDATION
LOCAL_PART_REGEX = '^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&*+-/=?^_`''{|}~\.]+$'
# MAIL_REGEX = '^[a-zA-Z0-9_!#$%&*+-/=?^_`''{|}~\.]*[a-zA-Z0-9_!#$%&*+-/=?^_`''{|}~]+@[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})$'
# DOMAIN_PART =
# MAIL_REGEX = '^' + LOCAL_PART + '@' +DOMAIN_PART + '$'

# ERROR MESSAGES
MSG_INVALID_MAIL = 'Invalid Email'
MSG_EMPTY_MAIL = 'Empty Email'
MSG_INVALID_PHONE = 'Invalid Phone'
MSG_NO_CONTACT_INFO = 'Empty Email and Empty Phone'
MSG_DISCARDED_CONTACT = 'Previously Discarded Contact'
MSG_INVALID_TYPE = 'Attribute "{}" invalid type'
MSG_INVALID_DOMAIN = 'Attribute "{}" invalid domain'
MSG_OUT_OF_RANGE = 'Attribute "{}" out of range [{},{}]'
