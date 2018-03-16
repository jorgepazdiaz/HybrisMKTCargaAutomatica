# -*- coding: utf-8 -*-
from mapping.contacts import I_PRIMER_NOMBRE, I_APE_PATERNO, I_TEL_MOVIL, \
    O_ID_ORIGIN, O_ID, O_NAME_FIRST, O_NAME_LAST, O_TELNR_MOBILE

# INTERACTION: Attribute names that will be loaded from the CSV
I_APP_TOKEN = 'App_Token'
I_MOBILE_APP = 'Mobile_App'

# MARKETING INTERACTION: List of attributes that the input file must include
I_FIELDS_APP_INSTALLED = [I_PRIMER_NOMBRE, I_APE_PATERNO, I_TEL_MOVIL, I_APP_TOKEN, I_MOBILE_APP]

# MARKETING INTERACTION: Attribute names used to store al info of the Marketing Interaction
O_COMM_MEDIUM = 'COMM_MEDIUM'
O_IA_TYPE = 'IA_TYPE'
O_TIMESTAMP = 'TIMESTAMP'
O_INTEREST_ITEM = 'INTEREST_ITEM'
O_CAMPAIGN_ID = 'CAMPAIGN_ID'
O_INITIATIVE_ID = 'INITIATIVE_ID'
O_INI_VERSION = 'INI_VERSION'
O_VALUATION = 'VALUATION'
O_IA_REASON = 'IA_REASON'
O_IS_ANONYMOUS = 'IS_ANONYMOUS'
O_AMOUNT = 'AMOUNT'
O_CURRENCY = 'CURRENCY'
O_LATITUDE = 'LATITUDE'
O_LONGITUDE = 'LONGITUDE'
O_SOURCE_OBJECT_TYPE = 'SOURCE_OBJECT_TYPE'
O_SOURCE_OBJECT_ID = 'SOURCE_OBJECT_ID'
O_SOURCE_OBJECT_ADD_ID = 'SOURCE_OBJECT_ADD_ID'
O_SOURCE_DATA_URL = 'SOURCE_DATA_URL'
O_CONTENT_TITLE = 'CONTENT_TITLE'
O_CONTENT_DATA = 'CONTENT_DATA'
O_MKT_AREA_ID = 'MKT_AREA_ID'
O_MKT_AGREEMENTORIGIN = 'MKT_AGREEMENTORIGIN'
O_MKT_AGREEMENTEXTERNALID = 'MKT_AGREEMENTEXTERNALID'
O_DEVICE_TYPE = 'DEVICE_TYPE'

# MARKETING INTERACTION: List of attributes that the output file must include
O_INTERACTION_FIELDS = [O_ID_ORIGIN, O_ID, O_COMM_MEDIUM, O_IA_TYPE, O_TIMESTAMP, O_INTEREST_ITEM,
                        O_CAMPAIGN_ID, O_INITIATIVE_ID, O_INI_VERSION, O_VALUATION, O_IA_REASON,
                        O_IS_ANONYMOUS, O_AMOUNT, O_CURRENCY, O_LATITUDE, O_LONGITUDE, O_SOURCE_OBJECT_TYPE,
                        O_SOURCE_OBJECT_ID, O_SOURCE_OBJECT_ADD_ID, O_SOURCE_DATA_URL, O_CONTENT_TITLE,
                        O_CONTENT_DATA, O_MKT_AREA_ID, O_MKT_AGREEMENTORIGIN, O_MKT_AGREEMENTEXTERNALID,
                        O_DEVICE_TYPE, O_NAME_FIRST, O_NAME_LAST, O_TELNR_MOBILE]

# MARKETING INTERACTION: File header needed to import
O_INTERACTION_FILE_HEADER =\
"""\
* User Instructions
* Enter the data for your upload directly below the header row starting at row 20.
* Do not delete the mandatory header row which contains an attribute name per column. You can change or add columns to the header row if you need to.
* You can define the order of the columns according to your requirements.
* Do not enter any data in columns that have no attribute name in the header row.
* Ensure that there are no empty rows above your data. Delete empty rows or enter an asterisk (*) at the start so that they are ignored for the upload.
* Comment rows are allowed only above the header row. They must start with an asterisk (*).
* Ensure that the header row contains no unknown attribute names (for example, due to typos). Unknown attribute names and the corresponding data are treated as comments and are ignored in the upload.
* As row separators, you can use <CRLF> for Windows systems and <CR> for Unix systems.
* As column separators, you can use a comma, semicolon, or tab.
* However, do not use separators (comma, semicolon, tab) in any text you enter in a cell.
* You can mask values using quotation marks or apostrophes. If you mask values, you must mask them in all columns.
* To prevent timestamp values from being automatically converted by the tool, you can change the cell format to number, without separators or decimal places. Please refer to the Microsoft Excel documentation for details of how to do this. Alternatively, you can make it a text by entering an apostrophe before the number.
* Before you can upload interests in the INTEREST_ITEM column, you must ensure that interests have already been created under Business Administration -> Interaction Interests.
* The maximum size of each upload file is 10 000, the recommended size is 5 000.
* Save the file as a CSV file.
* For more information, see the application help.
*
*
"""
