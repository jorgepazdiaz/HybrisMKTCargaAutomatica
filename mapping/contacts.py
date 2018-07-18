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


# MARKETING CONTACT: Mapping from contact CSV Import attributes (key) to ODATA Import attributes (values)
ODATA_CONTACT_MAPPING = {
    O_ID_ORIGIN: 'IdOrigin',
    O_ID: 'Id',
    O_NAME_FIRST: 'FirstName',
    O_NAME_LAST: 'LastName',
    O_TITLE_FT: 'TitleDescription',
    O_COUNTRY_FT: 'CountryDescription',
    O_CITY1: 'City',
    O_POSTCODE1: 'PostalCode',
    O_STREET: 'Street',
    O_HOUSE_NUM1: 'HouseNumber',
    O_SEX_FT: 'GenderDescription',
    O_CONSUMER_ACCOUNT_ID: 'SAPERPConsumerAccountId',
    O_COMPANY_NAME: 'CustomerName',
    O_COMPANY_ID_ORIGIN: 'CompanyIdOrigin',
    O_COMPANY_ID: 'CompanyId',
    O_SMTP_ADDR: 'EMailAddress',
    O_TELNR_LONG: 'PhoneNumber',
    O_TELNR_MOBILE: 'MobilePhoneNumber',
    O_DATE_OF_BIRTH: 'DateOfBirth',
    O_ID_TW: 'TwitterId',
    O_ID_FB: 'FacebookId',
    O_ID_GP: 'GooglePlusId',
    O_ID_ERP_CONTACT: 'SAPERPContactId',
    O_SMTP_ADDR_2: 'EMailAddress2',
    O_SMTP_ADDR_3: 'EMailAddress3',
    O_CODIGOEBELISTA: 'YY1_CodigoEbelista_MPS',
    O_DOCIDENTIDAD: 'YY1_DocumentoIdentidad_MPS'
}
