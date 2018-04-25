# -*- coding: utf-8 -*-
# CAMPAIGN INFO: Attribute names that will be loaded from the CSV
I_COD_EBELISTA = 'CodEbelista'
I_ANIO_CAMPANA_EXPOSICION = 'AnioCampanaExposicion'
I_ANIO_CAMPANA_PROCESO = 'AnioCampanaProceso'
I_ANIO_CAMPANA_INGRESO = 'AnioCampanaIngreso'
I_CAT_LANZAMIENTO = 'Categoria_Lanzamiento'
I_CAT_TOP = 'Categoria_Top'
I_COD_COMPORTAMIENTO = 'CodComportamiento'
I_COD_PAIS = 'CodPais'
I_COD_REGION = 'CodRegion'
I_COD_VTA_LANZAMIENTO = 'CodVenta_Lanzamiento'
I_COD_VTA_TOP = 'CodVenta_Top'
I_COD_ZONA = 'CodZona'
I_CUC_LANZAMIENTO = 'CUC_Lanzamiento'
I_CUC_TOP = 'CUC_Top'
I_DESC_CAT_SCORE = 'DesCategoriaScore'
I_DESC_CONSTANCIA_NUEVAS = 'DesConstanciaNuevas'
I_DESC_MARCA_SCORE = 'DesMarcaScore'
I_DESC_SEGMENTO = 'DesSegmento'
I_EDAD_BELCORP = 'EdadBelcorp'
I_FECHA_ENVIO = 'FechaEnvio'
I_FECHA_INICIO_FACTURACION = 'FechaInicioFacturacion'
I_FECHA_FIN_FACTURACION = 'FechaFinFacturacion'
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
I_FLAG_APP_CONS = 'FlagAppCons'
I_TOKEN_APP_CONS = 'TokenAppCons'
I_FLAG_APP_SOCIA = 'FlagAppSocia'
I_TOKEN_APP_SOCIA = 'TokenAppSocia'

# CAMPAIGN INFO: List of attributes that the input file must include
I_FIELDS_CAMPANAS_CONSULTORA = [I_COD_EBELISTA, I_ANIO_CAMPANA_EXPOSICION, I_ANIO_CAMPANA_PROCESO,
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
                                I_INVITACION_EMAIL_FICHA, I_INVITACION_EMAIL_LANDING, I_LINK_OFERTAS, I_FLAG_APP_CONS, I_TOKEN_APP_CONS,
                                I_FLAG_APP_SOCIA, I_TOKEN_APP_SOCIA]

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
O_FLAG_APP_CONS = 'FLAGAPPCONSULTORA'
O_TOKEN_APP_CONS = 'TOKENAPPCONSULTORA'
O_FLAG_APP_SOCIA = 'FLAGAPPSOCIA'
O_TOKEN_APP_SOCIA = 'TOKENAPPSOCIA'

# CAMPAIGN INFO: List of attributes that the output file must include
O_CAMPANA_CONSULTORA_FIELDS = [O_ANIO_CAMPANA_EXPOSICION, O_ANIO_CAMPANA_INGRESO, O_ANIO_CAMPANA_PROCESO, O_CUC_LANZAMIENTO,
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
                               O_INVITACION_SMS_FICHA, O_INVITACION_SMS_LANDING, O_INVITACION_EMAIL_FICHA, O_INVITACION_EMAIL_LANDING,
                               O_FLAG_APP_CONS, O_TOKEN_APP_CONS, O_FLAG_APP_SOCIA, O_TOKEN_APP_SOCIA]

# CAMPAIGN INFO: File header needed to import
O_CAMPANA_CONSULTORA_FILE_HEADER =\
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


# CAMPAIGN INFO: Mapping from contact CSV Import attributes (key) to ODATA Import attributes (values)
ODATA_CAMPANA_CONSULTORA_MAPPING = {
    O_IDORIGIN: 'ID_ORIGIN',
    O_ID_CAMPANA_CONSULTORA: 'IdCampanaConsultora',
    O_COD_EBELISTA: 'CodigoEbelista',
    O_ANIO_CAMPANA_EXPOSICION: 'AnioCampanaExposicion',
    O_NRO_CAMPANA_EXPOSICION: 'NumeroCampanaExposicion',
    O_ANIO_CAMPANA_PROCESO: 'AnioCampanaProceso',
    O_NRO_CAMPANA_PROCESO: 'NumeroCampanaProceso',
    O_ANIO_CAMPANA_INGRESO: 'AnioCampanaIngreso',
    O_NRO_CAMPANA_INGRESO: 'NumeroCampanaIngreso',
    O_CAT_LANZAMIENTO: 'CategoriaLanzamiento',
    O_CAT_TOP: 'CategoriaTop',
    O_COD_COMPORTAMIENTO: 'CodigoComportamiento',
    O_COD_PAIS: 'CodigoPais',
    O_COD_REGION: 'CodigoRegion',
    O_COD_VTA_LANZAMIENTO: 'CodigoVentaLanzamiento',
    O_COD_VTA_TOP: 'CodigoVentaTop',
    O_COD_ZONA: 'CodigoZona',
    O_CUC_LANZAMIENTO: 'CUCLanzamiento',
    O_CUC_TOP: 'CUCTop',
    O_DESC_CAT_SCORE: 'DescripcionCategoriaScore',
    O_DESC_CONSTANCIA_NUEVAS: 'DescripcionConstanciaNuevas',
    O_DESC_MARCA_SCORE: 'DescripcionMarcaScore',
    O_DESC_SEGMENTO: 'DescripcionSegmento',
    O_EDAD_BELCORP: 'EdadBelcorp',
    O_FECHA_ENVIO: 'FechaEnvio',
    O_FECHA_INICIO_FACTURACION: 'FechaInicioFacturacion',
    O_FECHA_FIN_FACTURACION: 'FechaFinFacturacion',
    O_FECHA_INICIO_VENTA: 'FechaInicioVenta',
    O_FECHA_FIN_VENTA: 'FechaFinVenta',
    O_FLAG_CELULAR: 'FlagCelular',
    O_FLAG_CONSTANCIA_NUEVAS: 'FlagConstanciaNuevas',
    O_FLAG_CORREO: 'FlagCorreo',
    O_FLAG_DEUDA: 'FlagDeuda',
    O_FLAG_INSCRITA: 'FlagInscrita',
    O_FLAG_IP_UNICO: 'FlagIPUnico',
    O_FLAG_OFERTA_DIGITAL_UC: 'FlagOfertaDigitalUC',
    O_FLAG_PASO_PEDIDO: 'FlagPasoPedido',
    O_FLAG_PASO_PEDIDO_CACT: 'FlagPasoPedidoCACT',
    O_FLAG_TP1: 'FlagTP1',
    O_FLAG_TP2: 'FlagTP2',
    O_IP_UNICO_PU5C: 'IPUnicoPU5C',
    O_MARCA_LANZAMIENTO: 'MarcaLanzamiento',
    O_MARCA_TOP: 'MarcaTop',
    O_MAX_VTA_FACTURADA_PU5C: 'MaxVentaFacturadaPU5C',
    O_MONTO_DEUDA: 'MontoDeuda',
    O_NRO_CAMPANA_NUEVAS: 'NumeroCampanaNuevas',
    O_NRO_PEDIDOS_NUEVAS: 'NumeroPedidosNuevas',
    O_OFERTA_DIGITAL_PU5C: 'OfertaDigitalPU5C',
    O_PROBABILIDAD_FUGA: 'ProbabilidadFuga',
    O_SCORE_CATEGORIA: 'ScoreCategoria',
    O_SCORE_LANZAMIENTO: 'ScoreLanzamiento',
    O_SCORE_MARCA: 'ScoreMarca',
    O_SCORE_MAS_CLIENTES: 'ScoreMasClientes',
    O_SCORE_TIP_COBRANZA: 'ScoreTipCobranza',
    O_SCORE_TIP_GESTION_DIGITAL: 'ScoreTipGestionDigital',
    O_SCORE_TIP_PEDIDO_ONLINE: 'ScoreTipPedidoOnLine',
    O_SCORE_TOP: 'ScoreTop',
    O_SCORE_VISITAS: 'ScoreVisitas',
    O_TIPO_CONSULTORA: 'TipoConsultora',
    O_VTA_FACTURADA_UC: 'VentaFacturadaUC',
    O_DESC_LANZAMIENTO: 'DescripcionLanzamiento',
    O_PRECIO_LANZAMIENTO: 'PrecioLanzamiento',
    O_LINK_LANZAMIENTO: 'LinkLanzamiento',
    O_DESC_TOP: 'DescripcionTop',
    O_PRECIO_TOP: 'PrecioTop',
    O_LINK_TOP: 'LinkTop',
    O_FLAG_INSCRITA_GANA_MAS: 'FlagInscritaGanaMas',
    O_INVITACION_SMS_FICHA: 'LinkInvitacionSMSFicha',
    O_INVITACION_SMS_LANDING: 'LinkInvitacionSMSLanding',
    O_INVITACION_EMAIL_FICHA: 'LinkInvitacionEmailFicha',
    O_INVITACION_EMAIL_LANDING: 'LinkInvitacionEmailLanding',
    O_LINK_OFERTAS: 'LinkOfertas',
    O_FLAG_APP_CONS: 'FlagAppConsultora',
    O_TOKEN_APP_CONS: 'TokenAppConsultora',
    O_FLAG_APP_SOCIA: 'FlagAppSocia',
    O_TOKEN_APP_SOCIA: 'TokenAppSocia'
}