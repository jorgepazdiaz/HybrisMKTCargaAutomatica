# -*- coding: utf-8 -*-
# MARKETING CONTACT: Attribute names that will be loaded from the CSV
I_DESC_PAIS = 'DesPais'
I_PRIMER_NOMBRE = 'PrimerNombre'
I_APE_PATERNO = 'DesApePaterno'
I_CORREO_ELECTRONICO = 'CorreoElectronico'
I_FECHA_NACIMIENTO = 'FechaNacimiento'
I_DOC_IDENTIDAD = 'DocIdentidad'
I_TEL_MOVIL = 'TelefonoMovil'

# MARKETING CONTACT: List of attributes that the input file must include
I_FIELDS_CONTACT = [I_DESC_PAIS, I_PRIMER_NOMBRE, I_APE_PATERNO, I_CORREO_ELECTRONICO,
                    I_FECHA_NACIMIENTO, I_DOC_IDENTIDAD, I_TEL_MOVIL]

# MARKETING CONTACT: Attribute names used to store al info of the Marketing Contacts
O_ID_ORIGIN = 'ID_ORIGIN'
O_ID = 'ID'
O_NAME_FIRST = 'NAME_FIRST'
O_NAME_LAST = 'NAME_LAST'
O_TITLE_FT = 'TITLE_FT'
O_COUNTRY_FT = 'COUNTRY_FT'
O_CITY1 = 'CITY1'
O_POSTCODE1 = 'POSTCODE1'
O_STREET = 'STREET'
O_HOUSE_NUM1 = 'HOUSE_NUM1'
O_SEX_FT = 'SEX_FT'
O_CONSUMER_ACCOUNT_ID = 'CONSUMER_ACCOUNT_ID'
O_COMPANY_NAME = 'COMPANY_NAME'
O_COMPANY_ID_ORIGIN = 'COMPANY_ID_ORIGIN'
O_COMPANY_ID = 'COMPANY_ID'
O_PAFKT_FT = 'PAFKT_FT'
O_SMTP_ADDR = 'SMTP_ADDR'
O_TELNR_LONG = 'TELNR_LONG'
O_TELNR_MOBILE = 'TELNR_MOBILE'
O_DATE_OF_BIRTH = 'DATE_OF_BIRTH'
O_ID_TW = 'ID_TW'
O_ID_FB = 'ID_FB'
O_ID_GP = 'ID_GP'
O_ID_ERP_CONTACT = 'ID_ERP_CONTACT'
O_SMTP_ADDR_2 = 'SMTP_ADDR_2'
O_SMTP_ADDR_3 = 'SMTP_ADDR_3'
O_CODIGOEBELISTA  = 'YY1_CODIGOEBELISTA_MPS'
O_DOCIDENTIDAD  = 'YY1_DocumentoIdentidad_MPS'
O_DISCARD_MOTIVE = 'DISCARD MOTIVE'

# MARKETING CONTACT: List of attributes that the output file must include
O_CONTACT_FIELDS = [O_ID_ORIGIN, O_ID, O_NAME_FIRST, O_NAME_LAST, O_TITLE_FT,
                    O_COUNTRY_FT, O_CITY1, O_POSTCODE1, O_STREET, O_HOUSE_NUM1,
                    O_SEX_FT, O_CONSUMER_ACCOUNT_ID, O_COMPANY_NAME, O_COMPANY_ID_ORIGIN,
                    O_COMPANY_ID, O_PAFKT_FT, O_SMTP_ADDR, O_TELNR_LONG, O_TELNR_MOBILE,
                    O_DATE_OF_BIRTH, O_ID_TW, O_ID_FB, O_ID_GP, O_ID_ERP_CONTACT,
                    O_SMTP_ADDR_2, O_SMTP_ADDR_3, O_CODIGOEBELISTA, O_DOCIDENTIDAD]


# MARKETING CONTACT: File header needed to import
O_CONTACT_FILE_HEADER =\
"""\
* User Instructions
* Enter the data for your upload directly below the header row starting at row 22.
* Do not delete the mandatory header row which contains an attribute name per column. You can change or add columns to the header row if you need to.
* If you need to change or add columns, the following additional columns might be relevant: ID_ORIGIN, LANGUAGE_FT, MARITAL_STATUS_FT, BRSCH_FT (Industry), ABTNR_FT(Department),PAFKT_FT (Contact Function),LATITUDE, LONGITUDE, SRID
* You can define the order of the columns according to your requirements.
* Do not enter any data in columns that have no attribute name in the header row.
* Ensure that there are no empty rows above your data. Delete empty rows or enter an asterisk (*) at the start so that they are ignored for the upload.
* Comment rows are allowed only above the header row. They must start with an asterisk (*).
* Ensure that the header row contains no unknown attribute names (for example, due to typos). Unknown attribute names and the corresponding data are treated as comments and are ignored in the upload.
* As row separators, you can use <CRLF> for Windows systems and <CR> for Unix systems.
* As column separators, you can use a comma, semicolon, or tab.
* However, do not use separators (comma, semicolon, tab) in any text you enter in a cell.
* You can mask values using quotation marks or apostrophes. If you mask values, you must mask them in all columns.
* If you want to upload the origin of contact IDs, you can add a column ID_ORIGIN to the structure. If the ID_ORIGIN is filled, the ID column must be filled too.
* Attributes containing codes (e.g. ISO codes for COUNTRY) are not allowed. The corresponding free text attributes (e.g. COUNTRY_FT United States) are allowed.
* The recommended maximum size of each upload file is 10000 records.
* Save the file as a CSV file.
* For more information, see the application help.
*
*
"""

# MARKETING CONTACT: Attribute names that will be loaded to Hybris Marketing using OData
S_ID_ORIGIN = 'IdOrigin'
S_ID = 'Id'
S_NAME_FIRST = 'FirstName'
S_NAME_LAST = 'LastName'
S_TITLE_FT = 'TitleDescription'
S_COUNTRY_FT = 'CountryDescription'
S_CITY1 = 'City'
S_POSTCODE1 = 'PostalCode'
S_STREET = 'Street'
S_HOUSE_NUM1 = 'HouseNumber'
S_SEX_FT = 'GenderDescription'
S_CONSUMER_ACCOUNT_ID = 'SAPERPConsumerAccountId'
S_COMPANY_NAME = 'CustomerName'
S_COMPANY_ID_ORIGIN = 'CompanyIdOrigin'
S_COMPANY_ID = 'CompanyId'
S_SMTP_ADDR = 'EMailAddress'
S_TELNR_LONG = 'PhoneNumber'
S_TELNR_MOBILE = 'MobilePhoneNumber'
S_DATE_OF_BIRTH = 'DateOfBirth'
S_ID_TW = 'TwitterId'
S_ID_FB = 'FacebookId'
S_ID_GP = 'GooglePlusId'
S_ID_ERP_CONTACT = 'SAPERPContactId'
S_SMTP_ADDR_2 = 'EMailAddress2'
S_SMTP_ADDR_3 = 'EMailAddress3'
S_CODIGOEBELISTA  = 'YY1_CodigoEbelista_MPS'
S_DOCIDENTIDAD  = 'YY1_DocumentoIdentidad_MPS'

# MARKETING CONTACT: List of attributes that the output service must include
S_FIELDS_CONTACT = [S_ID_ORIGIN, S_ID, S_NAME_FIRST, S_NAME_LAST, S_TITLE_FT,
                    S_COUNTRY_FT, S_CITY1, S_POSTCODE1, S_STREET, S_HOUSE_NUM1,
                    S_SEX_FT, S_CONSUMER_ACCOUNT_ID, S_COMPANY_NAME, S_COMPANY_ID_ORIGIN,
                    S_COMPANY_ID, S_SMTP_ADDR, S_TELNR_LONG, S_TELNR_MOBILE,
                    S_DATE_OF_BIRTH, S_ID_TW, S_ID_FB, S_ID_GP, S_ID_ERP_CONTACT,
                    S_SMTP_ADDR_2, S_SMTP_ADDR_3, S_CODIGOEBELISTA, S_DOCIDENTIDAD]

CONTACT_FIELDS = ['ID_ORIGIN', 'ID', 'NAME_FIRST', 'NAME_LAST', 'TITLE_FT',
                  'COUNTRY_FT', 'CITY1', 'POSTCODE1', 'STREET', 'HOUSE_NUM1',
                  'SEX_FT', 'CONSUMER_ACCOUNT_ID', 'COMPANY_NAME', 'COMPANY_ID_ORIGIN',
                  'COMPANY_ID', 'PAFKT_FT', 'SMTP_ADDR', 'TELNR_LONG', 'TELNR_MOBILE',
                  'DATE_OF_BIRTH', 'ID_TW', 'ID_FB', 'ID_GP', 'ID_ERP_CONTACT',
                  'SMTP_ADDR_2', 'SMTP_ADDR_3', 'CODIGOEBELISTA', 'DOCIDENTIDAD']

# O_CONTACT_FIELDS = [O_ID_ORIGIN, O_ID, O_NAME_FIRST, O_NAME_LAST, O_TITLE_FT,
#                     O_COUNTRY_FT, O_CITY1, O_POSTCODE1, O_STREET, O_HOUSE_NUM1,
#                     O_SEX_FT, O_CONSUMER_ACCOUNT_ID, O_COMPANY_NAME, O_COMPANY_ID_ORIGIN,
#                     O_COMPANY_ID, O_PAFKT_FT, O_SMTP_ADDR, O_TELNR_LONG, O_TELNR_MOBILE,
#                     O_DATE_OF_BIRTH, O_ID_TW, O_ID_FB, O_ID_GP, O_ID_ERP_CONTACT,
#                     O_SMTP_ADDR_2, O_SMTP_ADDR_3, O_CODIGOEBELISTA, O_DOCIDENTIDAD]


O_CODIGOEBELISTA  = 'YY1_CODIGOEBELISTA_MPS'
O_DOCIDENTIDAD  = 'YY1_DocumentoIdentidad_MPS'
