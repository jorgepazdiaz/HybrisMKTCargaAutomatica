# -*- coding: utf-8 -*-
# GENERAL SETTINGS
SOURCE_FOLDER = 'C:\IDATHA\PYXIS\BELCORP - Hybris Marketing\Datos\Recibidos\Sprint 5'
SOURCE_FILE = 'Estructura_Data_20180131_MOD_PRUEBA.csv'
OUTPUT_FOLDER =  'C:\IDATHA\PYXIS\BELCORP - Hybris Marketing\Datos\Transformados\Sprint 5'
MODE = 'PRODUCTIVE'
#MODE = 'TEST'
BATCH_SIZE = 5000
PHONE_REGEX = '^\+\d{11}$'
MAIL_REGEX = '^.+@[a-zA-Z0-9\-\.]+.([a-zA-Z]{2,3}|[0-9]{1,3})$'

#DOMAINS
D_MARCAS = ['L\'BEL', 'CYZONE', 'ESIKA']
D_CATEGORIAS = ['CP', 'MQ', 'TC', 'FG', 'TF']
D_CONSTANCIA_NUEVAS = ['C_1d1', 'C_2d2', 'C_3d3', 'C_4d4', 'C_5d5', 'C_6d6',
                       'I_1d1', 'I_1d2', 'I_1d3', 'I_1d4','I_1d5', 'I_1d6',
                       'I_2d2', 'I_2d3', 'I_2d4', 'I_2d5', 'I_2d6',
                       'I_3d3', 'I_3d4', 'I_3d5', 'I_3d6',
                       'I_4d4', 'I_4d5', 'I_4d6',
                       'I_5d5', 'I_5d6',
                       'I_6d6',
                       'Est', '0']
D_TIPO_CONSULTORA = ['E', 'N', 'R']
D_SEGMENTOS = [[0, 'Registradas'], [1, 'Nuevas'], [2, 'Brilla'], [3, 'Tops'], [4, 'Constantes 1'],
               [5, 'Constantes 2'], [6, 'Constantes 3'], [7, 'Inconstantes']]


# CAMPAIGN INFO: Attribute names that will be loaded from the CSV
I_COD_EBELISTA = 'Codebelista'
I_ANIO_CAMPANA_EXPOSICION = 'AnioCampanaExposicion'
I_ANIO_CAMPANA_PROCESO = 'AnioCampanaProceso'
I_ANIO_CAMPANA_INGRESO = 'AnioCampanaIngreso'
I_CAT_LANZAMIENTO = 'Categoria_Lanzamiento'
I_CAT_TOP = 'Categoria_Top'
I_COD_COMPORTAMIENTO = 'CodComportamiento'
I_COD_PAIS = 'Codpais'
I_COD_REGION = 'CodRegion'
I_COD_VTA_LANZAMIENTO = 'CodVenta_Lanzamiento'
I_COD_VTA_TOP = 'CodVenta_Top'
I_COD_ZONA = 'Codzona'
I_CUC_LANZAMIENTO = 'CUC_Lanzamiento'
I_CUC_TOP = 'CUC_Top'
I_DESC_CAT_SCORE = 'DesCategoriaScore'
I_DESC_CONSTANCIA_NUEVAS = 'DesConstanciaNuevas'
I_DESC_MARCA_SCORE = 'DesMarcaScore'
I_DESC_SEGMENTO = 'DesSegmento'
I_EDAD_BELCORP = 'EdadBelcorp'
I_FECHA_ENVIO = 'FechaEnvio'
I_FECHA_INICIO_FACTURACION = 'Fechainiciofacturacion'
I_FECHA_FIN_FACTURACION = 'Fechafinfacturacion'
I_FECHA_INICIO_VENTA = 'FechaInicioVenta'
I_FECHA_FIN_VENTA = 'FechaFinVenta'
I_FLAG_CELULAR = 'FlagCelular'
I_FLAG_CONSTANCIA_NUEVAS = 'FlagConstanciaNuevas'
I_FLAG_CORREO = 'FlagCorreo'
I_FLAG_DEUDA = 'FlagDeuda'
I_FLAG_INSCRITA = 'FlagInscrita'
I_FLAG_IP_UNICO = 'FlagIpUnico'
I_FLAG_OFERTA_DIGITAL_UC = 'FlagOfertaDigitalUC'
I_FLAG_PASO_PEDIDO = 'FlagPasoPedido'
I_FLAG_PASO_PEDIDO_CACT = 'FlagPasoPedidoCact'
I_FLAG_TP1 = 'FlagTP1'
I_FLAG_TP2 = 'FlagTP2'
I_IP_UNICO_PU5C = 'IpUnicoPU5C'
I_MARCA_LANZAMIENTO = 'Marca_Lanzamiento'
I_MARCA_TOP = 'Marca_Top'
I_MAX_VTA_FACTURADA_PU5C = 'MaxVentaFacturadaPU5C'
I_MONTO_DEUDA = 'MontoDeuda'
I_NRO_CAMPANA_NUEVAS = 'NroCampaniaNuevas'
I_NRO_PEDIDOS_NUEVAS = 'NroPedidosNuevas'
I_OFERTA_DIGITAL_PU5C = 'OfertaDigitalPU5C'
I_PROBABILIDAD_FUGA = 'ProbabilidadFuga'
I_SCORE_CATEGORIA = 'ScoreCategoria'
I_SCORE_LANZAMIENTO = 'ScoreLanzamiento'
I_SCORE_MARCA = 'ScoreMarca'
I_SCORE_MAS_CLIENTES = 'ScoreMasClientes'
I_SCORE_TIP_COBRANZA = 'ScoreTipCobranza'
I_SCORE_TIP_GESTION_DIGITAL = 'ScoreTipGestionDigital'
I_SCORE_TIP_PEDIDO_ONLINE = 'ScoreTipPedidoOnLine'
I_SCORE_TOP = 'ScoreTop'
I_SCORE_VISITAS = 'ScoreVisitas'
I_TIPO_CONSULTORA = 'TipoConsultora'
I_VTA_FACTURADA_UC = 'VentaFacturadaUC'
I_FLAG_INSCRITA_GANA_MAS = 'FlagInscritaGanaMas'
I_INVITACION_SMS_FICHA = 'Link_InvitacionSMS_Ficha'
I_INVITACION_SMS_LANDING = 'Link_InvitacionSMS_Landing'
I_INVITACION_EMAIL_FICHA = 'Link_InvitacionEmail_Ficha'
I_INVITACION_EMAIL_LANDING = 'Link_InvitacionEmail_Landing'
I_DESC_LANZAMIENTO = 'Descripcion_Lanzamiento'
I_PRECIO_LANZAMIENTO = 'Precio_Lanzamiento'
I_LINK_LANZAMIENTO = 'Link_Lanzamiento'
I_DESC_TOP = 'Descripcion_Top'
I_PRECIO_TOP = 'Precio_Top'
I_LINK_TOP = 'Link_Top'
I_LINK_OFERTAS = 'Link_Ofertas'

# CAMPAIGN INFO: List of attributes that the input file must include
# I_FIELDS_USU_CAMP = [I_COD_EBELISTA, I_ANIO_CAMPANA_EXPOSICION, I_ANIO_CAMPANA_PROCESO, I_ANIO_CAMPANA_INGRESO,
#                      I_CAT_LANZAMIENTO, I_CAT_TOP, I_COD_COMPORTAMIENTO, I_COD_PAIS, I_COD_REGION,
#                      I_COD_VTA_LANZAMIENTO, I_COD_VTA_TOP, I_COD_ZONA, I_CUC_LANZAMIENTO, I_CUC_TOP,
#                      I_DESC_CAT_SCORE, I_DESC_CONSTANCIA_NUEVAS, I_DESC_MARCA_SCORE, I_DESC_SEGMENTO,
#                      I_EDAD_BELCORP, I_FECHA_ENVIO, I_FECHA_INICIO_FACTURACION, I_FECHA_FIN_FACTURACION,
#                      I_FECHA_INICIO_VENTA, I_FECHA_FIN_VENTA, I_FLAG_CELULAR, I_FLAG_CONSTANCIA_NUEVAS,
#                      I_FLAG_CORREO, I_FLAG_DEUDA, I_FLAG_INSCRITA, I_FLAG_IP_UNICO, I_FLAG_OFERTA_DIGITAL_UC,
#                      I_FLAG_PASO_PEDIDO, I_FLAG_PASO_PEDIDO_CACT, I_FLAG_TP1, I_FLAG_TP2, I_IP_UNICO_PU5C,
#                      I_MARCA_LANZAMIENTO, I_MARCA_TOP, I_MAX_VTA_FACTURADA_PU5C, I_MONTO_DEUDA,
#                      I_NRO_CAMPANA_NUEVAS, I_NRO_PEDIDOS_NUEVAS, I_OFERTA_DIGITAL_PU5C, I_PROBABILIDAD_FUGA,
#                      I_SCORE_CATEGORIA, I_SCORE_LANZAMIENTO, I_SCORE_MARCA, I_SCORE_MAS_CLIENTES,
#                      I_SCORE_TIP_COBRANZA, I_SCORE_TIP_GESTION_DIGITAL, I_SCORE_TIP_PEDIDO_ONLINE, I_SCORE_TOP,
#                      I_SCORE_VISITAS, I_TIPO_CONSULTORA, I_VENTA_FACTURADA_UC,
#                      I_FLAG_INSCRITA_GANAMAS, I_INVITACION_SMS_FICHA, I_INVITACION_SMS_LANDING,
#                      I_INVITACION_EMAIL_FICHA, I_INVITACION_EMAIL_LANDING, I_DESC_LANZAMIENTO,
#                      I_PRECIO_LANZAMIENTO, I_LINK_LANZAMIENTO, I_DESC_TOP, I_PRECIO_TOP, I_LINK_TOP]

I_FIELDS_USU_CAMP = [I_COD_EBELISTA, I_ANIO_CAMPANA_EXPOSICION, I_ANIO_CAMPANA_PROCESO,
                     I_FECHA_ENVIO, I_COD_PAIS, I_COD_REGION, I_COD_ZONA, I_FECHA_INICIO_VENTA,
                     I_FECHA_FIN_VENTA, I_FECHA_INICIO_FACTURACION, I_FECHA_FIN_FACTURACION, I_TIPO_CONSULTORA,
                     I_DESC_SEGMENTO, I_COD_COMPORTAMIENTO, I_ANIO_CAMPANA_INGRESO,
                     I_EDAD_BELCORP, I_FLAG_PASO_PEDIDO, I_FLAG_IP_UNICO, I_SCORE_MARCA, I_SCORE_CATEGORIA, I_SCORE_TOP,
                     I_SCORE_LANZAMIENTO, I_SCORE_VISITAS, I_SCORE_TIP_GESTION_DIGITAL, I_SCORE_TIP_COBRANZA,
                     I_SCORE_MAS_CLIENTES, I_SCORE_TIP_PEDIDO_ONLINE, I_PROBABILIDAD_FUGA, I_DESC_CONSTANCIA_NUEVAS,
                     I_FLAG_CONSTANCIA_NUEVAS, I_NRO_PEDIDOS_NUEVAS, I_NRO_CAMPANA_NUEVAS, I_FLAG_TP1, I_FLAG_TP2,
                     I_IP_UNICO_PU5C, I_OFERTA_DIGITAL_PU5C, I_FLAG_OFERTA_DIGITAL_UC, I_MAX_VTA_FACTURADA_PU5C,
                     I_VTA_FACTURADA_UC, I_DESC_MARCA_SCORE, I_DESC_CAT_SCORE, I_COD_VTA_TOP,
                     I_CUC_TOP, I_MARCA_TOP, I_CAT_TOP, I_DESC_TOP, I_PRECIO_TOP, I_LINK_TOP,
                     I_COD_VTA_LANZAMIENTO, I_CUC_LANZAMIENTO, I_MARCA_LANZAMIENTO, I_CAT_LANZAMIENTO,
                     I_DESC_LANZAMIENTO, I_PRECIO_LANZAMIENTO, I_LINK_LANZAMIENTO, I_FLAG_PASO_PEDIDO_CACT,
                     I_FLAG_DEUDA, I_MONTO_DEUDA, I_FLAG_CORREO, I_FLAG_CELULAR, I_FLAG_INSCRITA,
                     I_FLAG_INSCRITA_GANA_MAS, I_INVITACION_SMS_FICHA, I_INVITACION_SMS_LANDING,
                     I_INVITACION_EMAIL_FICHA, I_INVITACION_EMAIL_LANDING, I_LINK_OFERTAS]

# CAMPAIGN INFO: Attribute names created in the Custom Business Object used to store the info relative to Campaigns
O_IDORIGIN = 'ID_ORIGIN'
O_ID_CAMPANA_CONSULTORA = 'IDCAMPANACONSULTORA'
O_COD_EBELISTA = 'CODIGOEBELISTA'
O_ANIO_CAMPANA_EXPOSICION = 'ANIOCAMPANAEXPOSICION'
O_NRO_CAMPANA_EXPOSICION = 'NUMEROCAMPANAEXPOSICION'
O_ANIO_CAMPANA_PROCESO = 'ANIOCAMPANAPROCESO'
O_NRO_CAMPANA_PROCESO = 'NUMEROCAMPANAPROCESO'
O_ANIO_CAMPANA_INGRESO = 'ANIOCAMPANAINGRESO'
O_NRO_CAMPANA_INGRESO = 'NUMEROCAMPANAINGRESO'
O_CAT_LANZAMIENTO = 'CATEGORIALANZAMIENTO'
O_CAT_TOP = 'CATEGORIATOP'
O_COD_COMPORTAMIENTO = 'CODIGOCOMPORTAMIENTO'
O_COD_PAIS = 'CODIGOPAIS'
O_COD_REGION = 'CODIGOREGION'
O_COD_VTA_LANZAMIENTO = 'CODIGOVENTALANZAMIENTO'
O_COD_VTA_TOP = 'CODIGOVENTATOP'
O_COD_ZONA = 'CODIGOZONA'
O_CUC_LANZAMIENTO = 'CUCLANZAMIENTO'
O_CUC_TOP = 'CUCTOP'
O_DESC_CAT_SCORE = 'DESCRIPCIONCATEGORIASCORE'
O_DESC_CONSTANCIA_NUEVAS = 'DESCRIPCIONCONSTANCIANUEVAS'
O_DESC_MARCA_SCORE = 'DESCRIPCIONMARCASCORE'
O_DESC_SEGMENTO = 'DESCRIPCIONSEGMENTO'
O_EDAD_BELCORP = 'EDADBELCORP'
O_FECHA_ENVIO = 'FECHAENVIO'
O_FECHA_INICIO_FACTURACION = 'FECHAINICIOFACTURACION'
O_FECHA_FIN_FACTURACION = 'FECHAFINFACTURACION'
O_FECHA_INICIO_VENTA = 'FECHAINICIOVENTA'
O_FECHA_FIN_VENTA = 'FECHAFINVENTA'
O_FLAG_CELULAR = 'FLAGCELULAR'
O_FLAG_CONSTANCIA_NUEVAS = 'FLAGCONSTANCIANUEVAS'
O_FLAG_CORREO = 'FLAGCORREO'
O_FLAG_DEUDA = 'FLAGDEUDA'
O_FLAG_INSCRITA = 'FLAGINSCRITA'
O_FLAG_IP_UNICO = 'FLAGIPUNICO'
O_FLAG_OFERTA_DIGITAL_UC = 'FLAGOFERTADIGITALUC'
O_FLAG_PASO_PEDIDO = 'FLAGPASOPEDIDO'
O_FLAG_PASO_PEDIDO_CACT = 'FLAGPASOPEDIDOCACT'
O_FLAG_TP1 = 'FLAGTP1'
O_FLAG_TP2 = 'FLAGTP2'
O_IP_UNICO_PU5C = 'IPUNICOPU5C'
O_MARCA_LANZAMIENTO = 'MARCALANZAMIENTO'
O_MARCA_TOP = 'MARCATOP'
O_MAX_VTA_FACTURADA_PU5C = 'MAXVENTAFACTURADAPU5C'
O_MONTO_DEUDA = 'MONTODEUDA'
O_NRO_CAMPANA_NUEVAS = 'NUMEROCAMPANANUEVAS'
O_NRO_PEDIDOS_NUEVAS = 'NUMEROPEDIDOSNUEVAS'
O_OFERTA_DIGITAL_PU5C = 'OFERTADIGITALPU5C'
O_PROBABILIDAD_FUGA = 'PROBABILIDADFUGA'
O_SCORE_CATEGORIA = 'SCORECATEGORIA'
O_SCORE_LANZAMIENTO = 'SCORELANZAMIENTO'
O_SCORE_MARCA = 'SCOREMARCA'
O_SCORE_MAS_CLIENTES = 'SCOREMASCLIENTES'
O_SCORE_TIP_COBRANZA = 'SCORETIPCOBRANZA'
O_SCORE_TIP_GESTION_DIGITAL = 'SCORETIPGESTIONDIGITAL'
O_SCORE_TIP_PEDIDO_ONLINE = 'SCORETIPPEDIDOONLINE'
O_SCORE_TOP = 'SCORETOP'
O_SCORE_VISITAS = 'SCOREVISITAS'
O_TIPO_CONSULTORA = 'TIPOCONSULTORA'
O_VTA_FACTURADA_UC = 'VENTAFACTURADAUC'
O_DESC_LANZAMIENTO = 'DESCRIPCIONLANZAMIENTO'
O_PRECIO_LANZAMIENTO = 'PRECIOLANZAMIENTO'
O_LINK_LANZAMIENTO = 'LINKLANZAMIENTO'
O_DESC_TOP = 'DESCRIPCIONTOP'
O_PRECIO_TOP = 'PRECIOTOP'
O_LINK_TOP = 'LINKTOP'
O_FLAG_INSCRITA_GANA_MAS = 'FLAGINSCRITAGANAMAS'
O_INVITACION_SMS_FICHA = 'LINKINVITACIONSMSFICHA'
O_INVITACION_SMS_LANDING = 'LINKINVITACIONSMSLANDING'
O_INVITACION_EMAIL_FICHA = 'LINKINVITACIONEMAILFICHA'
O_INVITACION_EMAIL_LANDING = 'LINKINVITACIONEMAILLANDING'
O_LINK_OFERTAS = 'LINKOFERTAS'

# CAMPAIGN INFO: List of attributes that the output file must include
# O_FIELDS_USU_CAMP = [O_IDORIGIN, O_ID_CAMPANA_CONSULTORA, O_COD_EBELISTA, O_ANIO_CAMPANA_EXPOSICION,
#                      O_NRO_CAMPANA_EXPOSICION, O_ANIO_CAMPANA_PROCESO, O_NRO_CAMPANA_PROCESO,
#                      O_ANIO_CAMPANA_INGRESO, O_NRO_CAMPANA_INGRESO, O_CAT_LANZAMIENTO, O_CAT_TOP,
#                      O_COD_COMPORTAMIENTO, O_COD_PAIS, O_COD_REGION, O_COD_VTA_LANZAMIENTO,
#                      O_COD_VTA_TOP, O_COD_ZONA, O_CUC_LANZAMIENTO, O_CUC_TOP, O_DESC_CAT_SCORE,
#                      O_DESC_CONSTANCIA_NUEVAS, O_DESC_MARCA_SCORE, O_DESC_SEGMENTO, O_EDAD_BELCORP,
#                      O_FECHA_ENVIO, O_FECHA_INICIO_FACTURACION, O_FECHA_FIN_FACTURACION, O_FECHA_INICIO_VENTA,
#                      O_FECHA_FIN_VENTA, O_FLAG_CELULAR, O_FLAG_CONSTANCIA_NUEVAS, O_FLAG_CORREO, O_FLAG_DEUDA,
#                      O_FLAG_INSCRITA, O_FLAG_IP_UNICO, O_FLAG_OFERTA_DIGITAL_UC, O_FLAG_PASO_PEDIDO,
#                      O_FLAG_PASO_PEDIDO_CACT, O_FLAG_TP1, O_FLAG_TP2, O_IP_UNICO_PU5C, O_MARCA_LANZAMIENTO,
#                      O_MARCA_TOP, O_MAX_VTA_FACTURADA_PU5C, O_MONTO_DEUDA, O_NRO_CAMPANA_NUEVAS,
#                      O_NRO_PEDIDOS_NUEVAS, O_OFERTA_DIGITAL_PU5C, O_PROBABILIDAD_FUGA, O_SCORE_CATEGORIA,
#                      O_SCORE_LANZAMIENTO, O_SCORE_MARCA, O_SCORE_MAS_CLIENTES, O_SCORE_TIP_COBRANZA,
#                      O_SCORE_TIP_GESTION_DIGITAL, O_SCORE_TIP_PEDIDO_ONLINE, O_SCORE_TOP, O_SCORE_VISITAS,
#                      O_TIPO_CONSULTORA, O_VENTA_FACTURADA_UC, O_FLAG_INSCRITA_GANAMAS, O_LINK_INVITACION_SMS_FICHA,
#                      O_LINK_INVITACION_SMS_LANDING, O_LINK_INVITACION_EMAIL_FICHA, O_LINK_INVITACION_EMAIL_LANDING,
#                      O_DESC_LANZAMIENTO, O_PRECIO_LANZAMIENTO, O_LINK_LANZAMIENTO, O_DESC_TOP, O_PRECIO_TOP,
#                      O_LINK_TOP]

O_FIELDS_USU_CAMP = [ O_ANIO_CAMPANA_EXPOSICION, O_ANIO_CAMPANA_INGRESO, O_ANIO_CAMPANA_PROCESO, O_CUC_LANZAMIENTO,
                      O_CUC_TOP, O_CAT_LANZAMIENTO, O_CAT_TOP, O_COD_COMPORTAMIENTO, O_COD_EBELISTA, O_COD_PAIS,
                      O_COD_REGION, O_COD_VTA_LANZAMIENTO, O_COD_VTA_TOP, O_COD_ZONA, O_DESC_CAT_SCORE,
                      O_DESC_CONSTANCIA_NUEVAS, O_DESC_LANZAMIENTO, O_DESC_MARCA_SCORE, O_DESC_SEGMENTO, O_DESC_TOP,
                      O_EDAD_BELCORP, O_FECHA_ENVIO, O_FECHA_FIN_FACTURACION, O_FECHA_FIN_VENTA,
                      O_FECHA_INICIO_FACTURACION, O_FECHA_INICIO_VENTA, O_FLAG_CELULAR, O_FLAG_CONSTANCIA_NUEVAS,
                      O_FLAG_CORREO, O_FLAG_DEUDA, O_FLAG_IP_UNICO, O_FLAG_INSCRITA, O_FLAG_INSCRITA_GANA_MAS,
                      O_FLAG_OFERTA_DIGITAL_UC, O_FLAG_PASO_PEDIDO, O_FLAG_PASO_PEDIDO_CACT, O_FLAG_TP1, O_FLAG_TP2,
                      O_IDORIGIN, O_IP_UNICO_PU5C, O_ID_CAMPANA_CONSULTORA,
                      O_LINK_LANZAMIENTO, O_LINK_OFERTAS, O_LINK_TOP, O_MARCA_LANZAMIENTO, O_MARCA_TOP,
                      O_MAX_VTA_FACTURADA_PU5C, O_MONTO_DEUDA, O_NRO_CAMPANA_EXPOSICION, O_NRO_CAMPANA_INGRESO,
                      O_NRO_CAMPANA_NUEVAS, O_NRO_CAMPANA_PROCESO, O_NRO_PEDIDOS_NUEVAS, O_OFERTA_DIGITAL_PU5C,
                      O_PRECIO_LANZAMIENTO, O_PRECIO_TOP, O_PROBABILIDAD_FUGA, O_SCORE_CATEGORIA, O_SCORE_LANZAMIENTO,
                      O_SCORE_MARCA, O_SCORE_MAS_CLIENTES, O_SCORE_TIP_COBRANZA, O_SCORE_TIP_GESTION_DIGITAL,
                      O_SCORE_TIP_PEDIDO_ONLINE, O_SCORE_TOP, O_SCORE_VISITAS, O_TIPO_CONSULTORA, O_VTA_FACTURADA_UC,
                      O_INVITACION_SMS_FICHA, O_INVITACION_SMS_LANDING, O_INVITACION_EMAIL_FICHA, O_INVITACION_EMAIL_LANDING]

O_CAMPANAS_CONSULTORAS_FILE_HEADER =\
"""\
* User Instructions:
* Row 17 displays the Custom Business Object ID. Do not delete this row.
* Row 19 displays the attribute descriptions per column.
* Row 20 displays the attribute name per column. Do not delete this header row.
* Row 21 displays the data type and length information for the attribute name per column. Enter the data for your upload directly starting at this row.
* Ensure that there are no empty rows above your data. Delete empty rows or enter an asterisk (*) at the start so that they are ignored for the upload.
* Comment rows are allowed only above the header row. They must start with an asterisk (*).
* Ensure that the header row contains no unknown attribute names (for example due to typos). Unknown attribute names and the corresponding data are treated as comments and are ignored in the upload.
* As row separators- you can use <CRLF> for Windows systems and <CR> for Unix systems.
* As column separators- you can use a comma / semicolon / tab.
* However do not use separators (comma / semicolon / tab) in any text you enter in a cell.
* You can mask values using quotation marks or apostrophes. If you mask values- you must mask them in all columns.
* The recommended maximum size of each upload file is 10000 records.
* Save the file as a CSV file.
* For more information, see the application help.
*
*Custom Business Object ID:YY1_CAMPANAS_CONSULTORA
*
*
"""

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

# MARKETING CONTACT: List of attributes that the output file must include
O_FIELDS_CONTACT = [O_ID_ORIGIN, O_ID, O_NAME_FIRST, O_NAME_LAST, O_TITLE_FT,
                    O_COUNTRY_FT, O_CITY1, O_POSTCODE1, O_STREET, O_HOUSE_NUM1,
                    O_SEX_FT, O_CONSUMER_ACCOUNT_ID, O_COMPANY_NAME, O_COMPANY_ID_ORIGIN,
                    O_COMPANY_ID, O_PAFKT_FT, O_SMTP_ADDR, O_TELNR_LONG, O_TELNR_MOBILE,
                    O_DATE_OF_BIRTH, O_ID_TW, O_ID_FB, O_ID_GP, O_ID_ERP_CONTACT,
                    O_SMTP_ADDR_2, O_SMTP_ADDR_3, O_CODIGOEBELISTA, O_DOCIDENTIDAD]


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

# INTERACTION: Attribute names that will be loaded from the CSV
I_APP_TOKEN = 'App_Token'

# MARKETING INTERACTION: List of attributes that the input file must include
I_FIELDS_INTERACT = [I_PRIMER_NOMBRE, I_APE_PATERNO, I_TEL_MOVIL, I_APP_TOKEN]

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
O_FIELDS_INTERACTION = [O_ID_ORIGIN, O_ID, O_COMM_MEDIUM, O_IA_TYPE, O_TIMESTAMP, O_INTEREST_ITEM,
                        O_CAMPAIGN_ID, O_INITIATIVE_ID, O_INI_VERSION, O_VALUATION, O_IA_REASON,
                        O_IS_ANONYMOUS, O_AMOUNT, O_CURRENCY, O_LATITUDE, O_LONGITUDE, O_SOURCE_OBJECT_TYPE,
                        O_SOURCE_OBJECT_ID, O_SOURCE_OBJECT_ADD_ID, O_SOURCE_DATA_URL, O_CONTENT_TITLE,
                        O_CONTENT_DATA, O_MKT_AREA_ID, O_MKT_AGREEMENTORIGIN, O_MKT_AGREEMENTEXTERNALID,
                        O_DEVICE_TYPE, O_NAME_FIRST, O_NAME_LAST, O_TELNR_MOBILE]

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

