# -*- coding: utf-8 -*-
import csv
import math
import decimal
from datetime import datetime
from common.settings import *
from common.domains import D_MARCAS, D_CATEGORIAS, D_CONSTANCIA_NUEVAS, D_TIPO_CONSULTORA, D_SEGMENTOS
from mapping.contacts import *
from mapping.campanas_consultoras import *
from mapping.interactions import *
import re
from validate_email import validate_email
from dal.dal import SqlServerAccess, ODataAccess
from dal.queries.virtual_coach_consultoras import VIRTUAL_COACH_CONSULTORAS_QUERY
from dal.conn_credentials import SQL_SERVER, SQL_DB
import os


def format_date(attribute, row):
    try:
        date = datetime.strftime(datetime.strptime(str(row[attribute]), '%Y%m%d'), '%Y%m%d')
        return date
    except ValueError:
        msg = MSG_INVALID_TYPE.format(attribute)
        raise Exception(msg)


def format_decimal(attribute, row, minimum=None, maximum=None):
    try:
        float_number = decimal.Decimal(row[attribute])
        if (minimum is not None and float_number < minimum) or \
                (maximum is not None and float_number > maximum):
            msg = MSG_OUT_OF_RANGE.format(attribute, minimum, maximum)
            raise Exception(msg)
        else:
            return '{:.10f}'.format(float_number)
    except ValueError:
        msg = MSG_INVALID_TYPE.format(attribute)
        raise Exception(msg)


def format_int(attribute, row, range):
    try:
        int_number = int(row[attribute])
        if int_number not in range:
            msg = MSG_OUT_OF_RANGE.format(attribute, min(list(range)), max(list(range)))
            raise Exception(msg)
        else:
            return int_number
    except ValueError:
        msg = MSG_INVALID_TYPE.format(attribute)
        raise Exception(msg)


def format_text(attribute, row):
    try:
        return row[attribute].replace('NULL', '').strip()
    except ValueError:
        msg = MSG_INVALID_TYPE.format(attribute)
        raise Exception(msg)


def format_phone(text_string):
    phone_string = str(text_string).strip()
    if phone_string != '':
        return '+' + phone_string
    else:
        return phone_string


def write_output_file(output_file, to_write, type, discard=False):
    try:
        if type not in OUTPUT_FILE_TYPES:
            msg = 'OUTPUT ERROR - Function argument type with value "{}" is not included in \{{}\}'.format(type, OUTPUT_FILE_TYPES)
            raise Exception(msg)
        elif type == PREFIX_CONTACT:
            fieldnames = O_CONTACT_FIELDS
            file_header = O_CONTACT_FILE_HEADER
        elif type == PREFIX_APP_INSTALLED:
            fieldnames = O_INTERACTION_FIELDS
            file_header = O_INTERACTION_FILE_HEADER
        elif type == PREFIX_CAMPANAS_CONSULTORA:
            fieldnames = O_CAMPANA_CONSULTORA_FIELDS
            file_header = O_CAMPANA_CONSULTORA_FILE_HEADER
        if discard:
            print('{} - Writing discarded file: {}'.format(type, output_file))
            discard_counter = 0
            with open(output_file.replace('.csv', '_DISCARDED.csv'), 'w', encoding="utf8") as ofile:
                fieldnames.copy()
                fieldnames.append(O_DISCARD_MOTIVE)
                # ofile.write(file_header)
                writer = csv.DictWriter(ofile, fieldnames=fieldnames, lineterminator='\n', delimiter=';')
                writer.writeheader()
                for item in to_write.values():
                    writer.writerow(item)
                    discard_counter += 1
                ofile.flush()
                ofile.close()
            print('{} - Lines discarded: {}'.format(type, discard_counter))
        else:
            print('{} - Writing output file(s): {}'.format(type, output_file))
            print('{} - Output fields: {}'.format(type, fieldnames))
            write_counter = 0
            max_files = math.ceil(len(to_write.values()) / BATCH_SIZE)
            to_write_values = list(to_write.values())
            for file_number in range(max_files):
                parcial_output_file = output_file.replace('.csv', '_{}.csv'.format(file_number))
                print('{} - Processing output file: {}'.format(type, parcial_output_file))
                with open(parcial_output_file, 'w', encoding='utf8') as ofile:
                    ofile.write(file_header)
                    writer = csv.DictWriter(ofile, fieldnames=fieldnames, lineterminator='\n', delimiter=';')
                    writer.writeheader()
                    ini_index = file_number * BATCH_SIZE
                    end_index = min((file_number + 1) * BATCH_SIZE, len(to_write_values))
                    for item in to_write_values[ini_index:end_index]:
                        writer.writerow(item)
                        write_counter += 1
                    ofile.flush()
                    ofile.close()
            print('{} - Lines written: {}'.format(type, write_counter))
    except ValueError as ve:
        print(ve)
        if item is not None:
            print(item)
        raise


def generate_contacts(contacts):
    contacts_to_write = {}
    contacts_to_discard = {}
    read_counter = 0
    for row in contacts:
        contact = {}
        for key in I_FIELDS_CONTACT:
            if key not in row.keys():
                msg = 'INPUT ERROR - Attribute "{}" is not included in the input file for row {}'.format(key, row.items())
                raise Exception(msg)
        contact[O_ID] = str(int(row[I_COD_EBELISTA])) + '_' + str(row[I_COD_PAIS])
        contact[O_NAME_FIRST] = format_text(I_PRIMER_NOMBRE, row)
        contact[O_NAME_LAST] = format_text(I_APE_PATERNO, row)
        contact[O_COUNTRY_FT] = format_text(I_DESC_PAIS, row)
        if MODE == 'PRODUCTIVE':
            contact[O_SMTP_ADDR] = str(row[I_CORREO_ELECTRONICO]).strip()
            # Debido a que datos enviados no cumlpen con formato no se carga este atributo
            # contact[O_TELNR_MOBILE] = format_phone(row[I_TEL_MOVIL])
        else:
            contact[O_SMTP_ADDR] = 'brunoo.gonzalez+{}@gmail.com'.format(read_counter+1)
        if row[I_FECHA_NACIMIENTO] != '':
            contact[O_DATE_OF_BIRTH] = format_date(I_FECHA_NACIMIENTO, row)
        contact[O_CODIGOEBELISTA] = int(row[I_COD_EBELISTA])
        contact[O_DOCIDENTIDAD] = format_text(I_DOC_IDENTIDAD, row)
        contact[O_ID_ORIGIN] = 'SAP_ODATA_IMPORT'
        for key in O_CONTACT_FIELDS:
            if key not in contact.keys():
                contact[key] = ''

        # Email & phone Validation
        is_valid_phone = re.search(PHONE_REGEX, contact[O_TELNR_MOBILE])
        is_valid_mail = validate_email(contact[O_SMTP_ADDR])
        discarded = contact.copy()
        if contact[O_SMTP_ADDR] == '':
            discarded[O_DISCARD_MOTIVE] = MSG_EMPTY_MAIL
            contacts_to_discard[contact[O_ID]] = discarded
        elif contact[O_SMTP_ADDR] != '':
            if not is_valid_mail:
                discarded[O_DISCARD_MOTIVE] = MSG_INVALID_MAIL
                contacts_to_discard[contact[O_ID]] = discarded
            else:
                [local_part, domain_part] = str(contact[O_SMTP_ADDR]).split('@',1)
                if not re.search(LOCAL_PART_REGEX, local_part):
                    discarded[O_DISCARD_MOTIVE] = MSG_INVALID_MAIL
                    contacts_to_discard[contact[O_ID]] = discarded
                else:
                    contacts_to_write[contact[O_ID]] = contact
        elif not (is_valid_phone or contact[O_TELNR_MOBILE] == ''):
            discarded[O_DISCARD_MOTIVE] = MSG_INVALID_PHONE
            contacts_to_discard[contact[O_ID]] = discarded
        else:
            contacts_to_write[contact[O_ID]] = contact
        read_counter += 1
    print('GENERAL - Lines read: {}'.format(read_counter))
    return contacts_to_write, contacts_to_discard


def generate_campanas_consultoras(campanas_consultoras, contacts):
    campanas_consultoras_to_write = {}
    campanas_consultoras_to_discard = {}
    read_counter = 0
    for row in campanas_consultoras:
        campana_consultora = {}
        discarded = {}
        read_counter += 1
        try:
            for key in I_FIELDS_CAMPANAS_CONSULTORA:
                if key not in row.keys():
                    msg = 'INPUT ERROR - Attribute "{}" is not included in the input file for row {}'.format(key,
                                                                                                             row.items())
                    raise Exception(msg)
                else:
                    discarded[key] = row[key]

            ## CUSTOM VALIDATIONS
            try:
                campana_consultora[O_COD_PAIS] = row[I_COD_PAIS]
                if len(campana_consultora[O_COD_PAIS]) != 2:
                    msg = MSG_INVALID_DOMAIN.format(I_COD_PAIS)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_COD_PAIS)
                raise Exception(msg)

            try:
                campana_consultora[O_COD_REGION] = format_text(I_COD_REGION, row)
                if len(str(campana_consultora[O_COD_REGION])) > 3:
                    msg = MSG_INVALID_DOMAIN.format(I_COD_REGION)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_COD_REGION)
                raise Exception(msg)

            try:
                campana_consultora[O_COD_ZONA] = int(row[I_COD_ZONA])
                if len(str(campana_consultora[O_COD_ZONA])) > 4:
                    msg = MSG_INVALID_DOMAIN.format(I_COD_ZONA)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_COD_ZONA)
                raise Exception(msg)

            try:
                campana_consultora[O_EDAD_BELCORP] = int(row[I_EDAD_BELCORP])
                if len(str(campana_consultora[O_EDAD_BELCORP])) > 4:
                    msg = MSG_INVALID_DOMAIN.format(I_EDAD_BELCORP)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_EDAD_BELCORP)
                raise Exception(msg)

            try:
                campana_consultora[O_COD_COMPORTAMIENTO] = int(row[I_COD_COMPORTAMIENTO])
                if campana_consultora[O_COD_COMPORTAMIENTO] not in range(0, 8):
                    msg = MSG_INVALID_DOMAIN.format(I_COD_COMPORTAMIENTO)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_COD_COMPORTAMIENTO)
                raise Exception(msg)

            try:
                campana_consultora[O_DESC_SEGMENTO] = row[I_DESC_SEGMENTO]
                if campana_consultora[O_DESC_SEGMENTO] not in [x[1] for x in D_SEGMENTOS]:
                    msg = MSG_INVALID_DOMAIN.format(I_DESC_SEGMENTO)
                    raise Exception(msg)
                else:
                    if [campana_consultora[O_COD_COMPORTAMIENTO], campana_consultora[O_DESC_SEGMENTO]] not in D_SEGMENTOS:
                        msg = 'Attributes "{}"-"{}" invalid tuple'.format(I_COD_COMPORTAMIENTO, I_DESC_SEGMENTO)
                        raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_DESC_SEGMENTO)
                raise Exception(msg)

            try:
                campana_consultora[O_TIPO_CONSULTORA] = row[I_TIPO_CONSULTORA]
                if campana_consultora[O_TIPO_CONSULTORA] not in D_TIPO_CONSULTORA:
                    msg = MSG_INVALID_DOMAIN.format(I_TIPO_CONSULTORA)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_TIPO_CONSULTORA)
                raise Exception(msg)

            try:
                campana_consultora[O_DESC_CONSTANCIA_NUEVAS] = row[I_DESC_CONSTANCIA_NUEVAS]
                if campana_consultora[O_DESC_CONSTANCIA_NUEVAS] != '' and \
                                campana_consultora[O_DESC_CONSTANCIA_NUEVAS] not in D_CONSTANCIA_NUEVAS:
                    msg = MSG_INVALID_DOMAIN.format(I_DESC_CONSTANCIA_NUEVAS)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_DESC_CONSTANCIA_NUEVAS)
                raise Exception(msg)

            try:
                campana_consultora[O_MARCA_LANZAMIENTO] = format_text(I_MARCA_LANZAMIENTO, row)
                if campana_consultora[O_MARCA_LANZAMIENTO] != '' and \
                                campana_consultora[O_MARCA_LANZAMIENTO] not in D_MARCAS:
                    msg = MSG_INVALID_DOMAIN.format(I_MARCA_LANZAMIENTO)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_MARCA_LANZAMIENTO)
                raise Exception(msg)

            try:
                campana_consultora[O_MARCA_TOP] = format_text(I_MARCA_TOP, row)
                if campana_consultora[O_MARCA_TOP] != '' and \
                                campana_consultora[O_MARCA_TOP] not in D_MARCAS:
                    msg = MSG_INVALID_DOMAIN.format(I_MARCA_TOP)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_MARCA_TOP)
                raise Exception(msg)

            try:
                campana_consultora[O_CAT_LANZAMIENTO] = format_text(I_CAT_LANZAMIENTO, row)
                if campana_consultora[O_CAT_LANZAMIENTO] != '' and \
                                campana_consultora[O_CAT_LANZAMIENTO] not in D_CATEGORIAS:
                    msg = MSG_INVALID_DOMAIN.format(I_CAT_LANZAMIENTO)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_CAT_LANZAMIENTO)
                raise Exception(msg)

            try:
                campana_consultora[O_CAT_TOP] = format_text(I_CAT_TOP, row)
                if campana_consultora[O_CAT_TOP] != '' and \
                                campana_consultora[O_CAT_TOP] not in D_CATEGORIAS:
                    msg = MSG_INVALID_DOMAIN.format(I_CAT_TOP)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_CAT_TOP)
                raise Exception(msg)

            try:
                campana_consultora[O_COD_VTA_LANZAMIENTO] = format_text(I_COD_VTA_LANZAMIENTO, row)
                if len(campana_consultora[O_COD_VTA_LANZAMIENTO]) not in range(0, 6):
                    msg = MSG_INVALID_DOMAIN.format(I_COD_VTA_LANZAMIENTO)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_COD_VTA_LANZAMIENTO)
                raise Exception(msg)

            try:
                campana_consultora[O_COD_VTA_TOP] = format_text(I_COD_VTA_TOP, row)
                if len(campana_consultora[O_COD_VTA_TOP]) not in range(0, 6):
                    msg = MSG_INVALID_DOMAIN.format(I_COD_VTA_TOP)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_COD_VTA_TOP)
                raise Exception(msg)

            try:
                campana_consultora[O_DESC_MARCA_SCORE] = format_text(I_DESC_MARCA_SCORE, row)
                if campana_consultora[O_DESC_MARCA_SCORE] == '0':
                    campana_consultora[O_DESC_MARCA_SCORE] = ''
                if campana_consultora[O_DESC_MARCA_SCORE] != '' and campana_consultora[O_DESC_MARCA_SCORE] not in D_MARCAS:
                    msg = MSG_INVALID_DOMAIN.format(I_DESC_MARCA_SCORE)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_DESC_MARCA_SCORE)
                raise Exception(msg)

            try:
                campana_consultora[O_DESC_CAT_SCORE] = format_text(I_DESC_CAT_SCORE, row)
                if campana_consultora[O_DESC_CAT_SCORE] == '0':
                    campana_consultora[O_DESC_CAT_SCORE] = ''
                if campana_consultora[O_DESC_CAT_SCORE] != '' and \
                                campana_consultora[O_DESC_CAT_SCORE] not in D_CATEGORIAS:
                    msg = MSG_INVALID_DOMAIN.format(I_DESC_CAT_SCORE)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_DESC_CAT_SCORE)
                raise Exception(msg)

            ## INTEGERS
            try:
                campana_consultora[O_ANIO_CAMPANA_EXPOSICION] = int(row[I_ANIO_CAMPANA_EXPOSICION][0:4])
                campana_consultora[O_NRO_CAMPANA_EXPOSICION] = int(row[I_ANIO_CAMPANA_EXPOSICION][4:6])
                if campana_consultora[O_NRO_CAMPANA_EXPOSICION] not in range(1, 19):
                    msg = MSG_INVALID_DOMAIN.format(I_ANIO_CAMPANA_EXPOSICION)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_ANIO_CAMPANA_EXPOSICION)
                raise Exception(msg)
            try:
                campana_consultora[O_ANIO_CAMPANA_INGRESO] = int(row[I_ANIO_CAMPANA_INGRESO][0:4])
                campana_consultora[O_NRO_CAMPANA_INGRESO] = int(row[I_ANIO_CAMPANA_INGRESO][4:6])
                if campana_consultora[O_NRO_CAMPANA_INGRESO] not in range(1, 19):
                    msg = MSG_INVALID_DOMAIN.format(I_ANIO_CAMPANA_INGRESO)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(I_ANIO_CAMPANA_INGRESO)
                raise Exception(msg)
            try:
                campana_consultora[O_ANIO_CAMPANA_PROCESO] = int(row[I_ANIO_CAMPANA_PROCESO][0:4])
                campana_consultora[O_NRO_CAMPANA_PROCESO] = int(row[I_ANIO_CAMPANA_PROCESO][4:6])
                if campana_consultora[O_NRO_CAMPANA_PROCESO] not in range(1, 19):
                    msg = MSG_INVALID_DOMAIN.format(O_NRO_CAMPANA_PROCESO)
                    raise Exception(msg)
            except ValueError:
                msg = MSG_INVALID_TYPE.format(O_NRO_CAMPANA_PROCESO)
                raise Exception(msg)
            try:
                campana_consultora[O_NRO_CAMPANA_NUEVAS] = format_int(I_NRO_CAMPANA_NUEVAS, row, range(0, 7))
                campana_consultora[O_NRO_PEDIDOS_NUEVAS] = format_int(I_NRO_PEDIDOS_NUEVAS, row, range(0, 7))
                campana_consultora[O_IP_UNICO_PU5C] = format_int(I_IP_UNICO_PU5C, row, range(0, 6))
                campana_consultora[O_OFERTA_DIGITAL_PU5C] = format_int(I_OFERTA_DIGITAL_PU5C, row, range(0, 7))
                campana_consultora[O_FLAG_CONSTANCIA_NUEVAS] = format_int(I_FLAG_CONSTANCIA_NUEVAS, row, range(-1, 2))
                campana_consultora[O_FLAG_TP1] = format_int(I_FLAG_TP1, row, range(-1, 2))
                campana_consultora[O_FLAG_TP2] = format_int(I_FLAG_TP2, row, range(-1, 2))
                campana_consultora[O_FLAG_IP_UNICO] = format_int(I_FLAG_IP_UNICO, row, range(0, 2))
                campana_consultora[O_FLAG_PASO_PEDIDO_CACT] = format_int(I_FLAG_PASO_PEDIDO_CACT, row, range(0, 2))
                campana_consultora[O_FLAG_DEUDA] = format_int(I_FLAG_DEUDA, row, range(0, 2))
                campana_consultora[O_FLAG_CORREO] = format_int(I_FLAG_CORREO, row, range(0, 2))
                campana_consultora[O_FLAG_CELULAR] = format_int(I_FLAG_CELULAR, row, range(0, 2))
                campana_consultora[O_FLAG_INSCRITA] = format_int(I_FLAG_INSCRITA, row, range(0, 3))
                campana_consultora[O_FLAG_OFERTA_DIGITAL_UC] = format_int(I_FLAG_OFERTA_DIGITAL_UC, row, range(0, 2))
                campana_consultora[O_FLAG_PASO_PEDIDO] = format_int(I_FLAG_PASO_PEDIDO, row, range(0, 2))
                campana_consultora[O_FLAG_INSCRITA_GANA_MAS] = format_int(I_FLAG_INSCRITA_GANA_MAS, row, range(0, 3))

                ## DATES
                campana_consultora[O_FECHA_INICIO_VENTA] = format_date(I_FECHA_INICIO_VENTA, row)
                campana_consultora[O_FECHA_FIN_VENTA] = format_date(I_FECHA_FIN_VENTA, row)
                campana_consultora[O_FECHA_INICIO_FACTURACION] = format_date(I_FECHA_INICIO_FACTURACION, row)
                campana_consultora[O_FECHA_FIN_FACTURACION] = format_date(I_FECHA_FIN_FACTURACION, row)
                campana_consultora[O_FECHA_ENVIO] = format_date(I_FECHA_ENVIO, row)

                ## DECIMALS
                campana_consultora[O_SCORE_MARCA] = format_decimal(I_SCORE_MARCA, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_CATEGORIA] = format_decimal(I_SCORE_CATEGORIA, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TOP] = format_decimal(I_SCORE_TOP, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_LANZAMIENTO] = format_decimal(I_SCORE_LANZAMIENTO, row, minimum=0.0, maximum=1000.0)
                campana_consultora[O_SCORE_VISITAS] = format_decimal(I_SCORE_VISITAS, row, minimum=0.0, maximum=1000.0)
                campana_consultora[O_SCORE_TIP_GESTION_DIGITAL] = format_decimal(I_SCORE_TIP_GESTION_DIGITAL, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TIP_COBRANZA] = format_decimal(I_SCORE_TIP_COBRANZA, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_MAS_CLIENTES] = format_decimal(I_SCORE_MAS_CLIENTES, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TIP_PEDIDO_ONLINE] = format_decimal(I_SCORE_TIP_PEDIDO_ONLINE, row)
                campana_consultora[O_PROBABILIDAD_FUGA] = format_decimal(I_PROBABILIDAD_FUGA, row, minimum=0.0, maximum=100.0)
                campana_consultora[O_VTA_FACTURADA_UC] = format_decimal(I_VTA_FACTURADA_UC, row)
                campana_consultora[O_PRECIO_LANZAMIENTO] = format_decimal(I_PRECIO_LANZAMIENTO, row)
                campana_consultora[O_PRECIO_TOP] = format_decimal(I_PRECIO_TOP, row)
                campana_consultora[O_MONTO_DEUDA] = format_decimal(I_MONTO_DEUDA, row)
                campana_consultora[O_MAX_VTA_FACTURADA_PU5C] = format_decimal(I_MAX_VTA_FACTURADA_PU5C, row)

                ## TEXTS
                campana_consultora[O_CUC_LANZAMIENTO] = format_text(I_CUC_LANZAMIENTO, row)
                campana_consultora[O_CUC_TOP] = format_text(I_CUC_TOP, row)
                campana_consultora[O_DESC_LANZAMIENTO] = format_text(I_DESC_LANZAMIENTO, row)
                campana_consultora[O_LINK_LANZAMIENTO] = format_text(I_LINK_LANZAMIENTO, row)
                campana_consultora[O_DESC_TOP] = format_text(I_DESC_TOP, row)
                campana_consultora[O_LINK_TOP] = format_text(I_LINK_TOP, row)
                campana_consultora[O_INVITACION_SMS_FICHA] = format_text(I_INVITACION_SMS_FICHA, row)
                campana_consultora[O_INVITACION_SMS_LANDING] = format_text(I_INVITACION_SMS_LANDING, row)
                campana_consultora[O_INVITACION_EMAIL_FICHA] = format_text(I_INVITACION_EMAIL_FICHA, row)
                campana_consultora[O_INVITACION_EMAIL_LANDING] = format_text(I_INVITACION_EMAIL_LANDING, row)
                campana_consultora[O_LINK_OFERTAS] = format_text(I_LINK_OFERTAS, row)
            except ValueError as ve:
                msg = ve.args[0]
                raise Exception(msg)

            if len(str(int(row[I_COD_EBELISTA]))) > 15:
                msg = MSG_INVALID_DOMAIN.format(I_COD_EBELISTA)
                raise Exception(msg)
            campana_consultora[O_COD_EBELISTA] = str(int(row[I_COD_EBELISTA])) + '_' + \
                                                 str(campana_consultora[O_COD_PAIS])
            campana_consultora[O_ID_CAMPANA_CONSULTORA] = str(campana_consultora[O_ANIO_CAMPANA_EXPOSICION]) + \
                                                          str(campana_consultora[O_NRO_CAMPANA_EXPOSICION]).zfill(2) + '_' + \
                                                          str(campana_consultora[O_COD_EBELISTA])
            campana_consultora[O_IDORIGIN] = 'SAP_ODATA_IMPORT'
            if campana_consultora[O_COD_EBELISTA] in contacts:
                campanas_consultoras_to_write[campana_consultora[O_ID_CAMPANA_CONSULTORA]] = campana_consultora
            else:
                discarded = campana_consultora.copy()
                discarded[O_DISCARD_MOTIVE] = MSG_DISCARDED_CONTACT
                campanas_consultoras_to_discard[discarded[O_ID_CAMPANA_CONSULTORA]] = discarded
        except ValueError as ve:
            discarded = campana_consultora.copy()
            if O_COD_PAIS not in discarded.keys():
                discarded[O_COD_PAIS] = row[I_COD_PAIS]
            if O_COD_REGION not in discarded.keys():
                discarded[O_COD_REGION] = row[I_COD_REGION]
            if O_COD_ZONA not in discarded.keys():
                discarded[O_COD_ZONA] = row[I_COD_ZONA]
            if O_EDAD_BELCORP not in discarded.keys():
                discarded[O_EDAD_BELCORP] = row[I_EDAD_BELCORP]
            if O_COD_COMPORTAMIENTO not in discarded.keys():
                discarded[O_COD_COMPORTAMIENTO] = row[I_COD_COMPORTAMIENTO]
            if O_DESC_SEGMENTO not in discarded.keys():
                discarded[O_DESC_SEGMENTO] = row[I_DESC_SEGMENTO]
            if O_TIPO_CONSULTORA not in discarded.keys():
                discarded[O_TIPO_CONSULTORA] = row[I_TIPO_CONSULTORA]
            if O_DESC_CONSTANCIA_NUEVAS not in discarded.keys():
                discarded[O_DESC_CONSTANCIA_NUEVAS] = row[I_DESC_CONSTANCIA_NUEVAS]
            if O_MARCA_LANZAMIENTO not in discarded.keys():
                discarded[O_MARCA_LANZAMIENTO] = row[I_MARCA_LANZAMIENTO]
            if O_MARCA_TOP not in discarded.keys():
                discarded[O_MARCA_TOP] = row[I_MARCA_TOP]
            if O_CAT_LANZAMIENTO not in discarded.keys():
                discarded[O_CAT_LANZAMIENTO] = row[I_CAT_LANZAMIENTO]
            if O_CAT_TOP not in discarded.keys():
                discarded[O_CAT_TOP] = row[I_CAT_TOP]
            if O_COD_VTA_LANZAMIENTO not in discarded.keys():
                discarded[O_COD_VTA_LANZAMIENTO] = row[I_COD_VTA_LANZAMIENTO]
            if O_COD_VTA_TOP not in discarded.keys():
                discarded[O_COD_VTA_TOP] = row[I_COD_VTA_TOP]
            if O_DESC_MARCA_SCORE not in discarded.keys():
                discarded[O_DESC_MARCA_SCORE] = row[I_DESC_MARCA_SCORE]
            if O_DESC_CAT_SCORE not in discarded.keys():
                discarded[O_DESC_CAT_SCORE] = row[I_DESC_CAT_SCORE]
            if O_ANIO_CAMPANA_EXPOSICION not in discarded.keys():
                discarded[O_ANIO_CAMPANA_EXPOSICION] = row[I_ANIO_CAMPANA_EXPOSICION][0:4]
            if O_NRO_CAMPANA_EXPOSICION not in discarded.keys():
                discarded[O_NRO_CAMPANA_EXPOSICION] = row[I_ANIO_CAMPANA_EXPOSICION][4:6]
            if O_ANIO_CAMPANA_INGRESO not in discarded.keys():
                discarded[O_ANIO_CAMPANA_INGRESO] = row[I_ANIO_CAMPANA_INGRESO][0:4]
            if O_NRO_CAMPANA_INGRESO not in discarded.keys():
                discarded[O_NRO_CAMPANA_INGRESO] = row[I_ANIO_CAMPANA_INGRESO][4:6]
            if O_ANIO_CAMPANA_PROCESO not in discarded.keys():
                discarded[O_ANIO_CAMPANA_PROCESO] = row[I_ANIO_CAMPANA_PROCESO][0:4]
            if O_NRO_CAMPANA_PROCESO not in discarded.keys():
                discarded[O_NRO_CAMPANA_PROCESO] = row[I_ANIO_CAMPANA_PROCESO][4:6]
            if O_NRO_CAMPANA_NUEVAS not in discarded.keys():
                discarded[O_NRO_CAMPANA_NUEVAS] = row[I_NRO_CAMPANA_NUEVAS]
            if O_NRO_PEDIDOS_NUEVAS not in discarded.keys():
                discarded[O_NRO_PEDIDOS_NUEVAS] = row[I_NRO_PEDIDOS_NUEVAS]
            if O_IP_UNICO_PU5C not in discarded.keys():
                discarded[O_IP_UNICO_PU5C] = row[I_IP_UNICO_PU5C]
            if O_OFERTA_DIGITAL_PU5C not in discarded.keys():
                discarded[O_OFERTA_DIGITAL_PU5C] = row[I_OFERTA_DIGITAL_PU5C]
            if O_FLAG_CONSTANCIA_NUEVAS not in discarded.keys():
                discarded[O_FLAG_CONSTANCIA_NUEVAS] = row[I_FLAG_CONSTANCIA_NUEVAS]
            if O_FLAG_TP1 not in discarded.keys():
                discarded[O_FLAG_TP1] = row[I_FLAG_TP1]
            if O_FLAG_TP2 not in discarded.keys():
                discarded[O_FLAG_TP2] = row[I_FLAG_TP2]
            if O_FLAG_IP_UNICO not in discarded.keys():
                discarded[O_FLAG_IP_UNICO] = row[I_FLAG_IP_UNICO]
            if O_FLAG_PASO_PEDIDO_CACT not in discarded.keys():
                discarded[O_FLAG_PASO_PEDIDO_CACT] = row[I_FLAG_PASO_PEDIDO_CACT]
            if O_FLAG_DEUDA not in discarded.keys():
                discarded[O_FLAG_DEUDA] = row[I_FLAG_DEUDA]
            if O_FLAG_CORREO not in discarded.keys():
                discarded[O_FLAG_CORREO] = row[I_FLAG_CORREO]
            if O_FLAG_CELULAR not in discarded.keys():
                discarded[O_FLAG_CELULAR] = row[I_FLAG_CELULAR]
            if O_FLAG_INSCRITA not in discarded.keys():
                discarded[O_FLAG_INSCRITA] = row[I_FLAG_INSCRITA]
            if O_FLAG_OFERTA_DIGITAL_UC not in discarded.keys():
                discarded[O_FLAG_OFERTA_DIGITAL_UC] = row[I_FLAG_OFERTA_DIGITAL_UC]
            if O_FLAG_PASO_PEDIDO not in discarded.keys():
                discarded[O_FLAG_PASO_PEDIDO] = row[I_FLAG_PASO_PEDIDO]
            if O_FLAG_INSCRITA_GANA_MAS not in discarded.keys():
                discarded[O_FLAG_INSCRITA_GANA_MAS] = row[I_FLAG_INSCRITA_GANA_MAS]
            if O_FECHA_INICIO_VENTA not in discarded.keys():
                discarded[O_FECHA_INICIO_VENTA] = row[I_FECHA_INICIO_VENTA]
            if O_FECHA_FIN_VENTA not in discarded.keys():
                discarded[O_FECHA_FIN_VENTA] = row[I_FECHA_FIN_VENTA]
            if O_FECHA_INICIO_FACTURACION not in discarded.keys():
                discarded[O_FECHA_INICIO_FACTURACION] = row[I_FECHA_INICIO_FACTURACION]
            if O_FECHA_FIN_FACTURACION not in discarded.keys():
                discarded[O_FECHA_FIN_FACTURACION] = row[I_FECHA_FIN_FACTURACION]
            if O_FECHA_ENVIO not in discarded.keys():
                discarded[O_FECHA_ENVIO] = row[I_FECHA_ENVIO]
            if O_SCORE_MARCA not in discarded.keys():
                discarded[O_SCORE_MARCA] = row[I_SCORE_MARCA]
            if O_SCORE_CATEGORIA not in discarded.keys():
                discarded[O_SCORE_CATEGORIA] = row[I_SCORE_CATEGORIA]
            if O_SCORE_TOP not in discarded.keys():
                discarded[O_SCORE_TOP] = row[I_SCORE_TOP]
            if O_SCORE_LANZAMIENTO not in discarded.keys():
                discarded[O_SCORE_LANZAMIENTO] = row[I_SCORE_LANZAMIENTO]
            if O_SCORE_VISITAS not in discarded.keys():
                discarded[O_SCORE_VISITAS] = row[I_SCORE_VISITAS]
            if O_SCORE_TIP_GESTION_DIGITAL not in discarded.keys():
                discarded[O_SCORE_TIP_GESTION_DIGITAL] = row[I_SCORE_TIP_GESTION_DIGITAL]
            if O_SCORE_TIP_COBRANZA not in discarded.keys():
                discarded[O_SCORE_TIP_COBRANZA] = row[I_SCORE_TIP_COBRANZA]
            if O_SCORE_MAS_CLIENTES not in discarded.keys():
                discarded[O_SCORE_MAS_CLIENTES] = row[I_SCORE_MAS_CLIENTES]
            if O_SCORE_TIP_PEDIDO_ONLINE not in discarded.keys():
                discarded[O_SCORE_TIP_PEDIDO_ONLINE] = row[I_SCORE_TIP_PEDIDO_ONLINE]
            if O_PROBABILIDAD_FUGA not in discarded.keys():
                discarded[O_PROBABILIDAD_FUGA] = row[I_PROBABILIDAD_FUGA]
            if O_VTA_FACTURADA_UC not in discarded.keys():
                discarded[O_VTA_FACTURADA_UC] = row[I_VTA_FACTURADA_UC]
            if O_PRECIO_LANZAMIENTO not in discarded.keys():
                discarded[O_PRECIO_LANZAMIENTO] = row[I_PRECIO_LANZAMIENTO]
            if O_PRECIO_TOP not in discarded.keys():
                discarded[O_PRECIO_TOP] = row[I_PRECIO_TOP]
            if O_MONTO_DEUDA not in discarded.keys():
                discarded[O_MONTO_DEUDA] = row[I_MONTO_DEUDA]
            if O_MAX_VTA_FACTURADA_PU5C not in discarded.keys():
                discarded[O_MAX_VTA_FACTURADA_PU5C] = row[I_MAX_VTA_FACTURADA_PU5C]
            if O_CUC_LANZAMIENTO not in discarded.keys():
                discarded[O_CUC_LANZAMIENTO] = row[I_CUC_LANZAMIENTO]
            if O_CUC_TOP not in discarded.keys():
                discarded[O_CUC_TOP] = row[I_CUC_TOP]
            if O_DESC_LANZAMIENTO not in discarded.keys():
                discarded[O_DESC_LANZAMIENTO] = row[I_DESC_LANZAMIENTO]
            if O_LINK_LANZAMIENTO not in discarded.keys():
                discarded[O_LINK_LANZAMIENTO] = row[I_LINK_LANZAMIENTO]
            if O_DESC_TOP not in discarded.keys():
                discarded[O_DESC_TOP] = row[I_DESC_TOP]
            if O_LINK_TOP not in discarded.keys():
                discarded[O_LINK_TOP] = row[I_LINK_TOP]
            if O_INVITACION_SMS_FICHA not in discarded.keys():
                discarded[O_INVITACION_SMS_FICHA] = row[I_INVITACION_SMS_FICHA]
            if O_INVITACION_SMS_LANDING not in discarded.keys():
                discarded[O_INVITACION_SMS_LANDING] = row[I_INVITACION_SMS_LANDING]
            if O_INVITACION_EMAIL_FICHA not in discarded.keys():
                discarded[O_INVITACION_EMAIL_FICHA] = row[I_INVITACION_EMAIL_FICHA]
            if O_INVITACION_EMAIL_LANDING not in discarded.keys():
                discarded[O_INVITACION_EMAIL_LANDING] = row[I_INVITACION_EMAIL_LANDING]
            if O_LINK_OFERTAS not in discarded.keys():
                discarded[O_LINK_OFERTAS] = row[I_LINK_OFERTAS]
            if O_COD_EBELISTA not in discarded.keys():
                discarded[O_COD_EBELISTA] = str(row[I_COD_EBELISTA]) + '_' + \
                                            str(campana_consultora[O_COD_PAIS])
            if O_ID_CAMPANA_CONSULTORA not in discarded.keys():
                    discarded[O_ID_CAMPANA_CONSULTORA] = str(row[O_ANIO_CAMPANA_EXPOSICION]) + \
                                                         str(row[O_NRO_CAMPANA_EXPOSICION]).zfill(2) + '_' + \
                                                         str(row[O_COD_EBELISTA])
            if O_IDORIGIN not in discarded.keys():
                discarded[O_IDORIGIN] = 'SAP_ODATA_IMPORT'
            discarded[O_DISCARD_MOTIVE] = ve.args[0]
            campanas_consultoras_to_discard[discarded[O_ID_CAMPANA_CONSULTORA]] = discarded

    return campanas_consultoras_to_write, campanas_consultoras_to_discard


def import_csv(source_folder, source_file, output_folder):
    try:
        input_file = os.path.join(source_folder, source_file)
        print('GENERAL - Opening input file: {}'.format(input_file))
        with open(input_file, 'r', encoding=SOURCE_ENCODING) as ifile:
            print('{} - Required fields: {}'.format(PREFIX_CONTACT, I_FIELDS_CONTACT))
            reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
            contacts_to_write, contacts_to_discard = generate_contacts(reader)
        output_file = os.path.join(output_folder, PREFIX_CONTACT + '_' + source_file)
        write_output_file(output_file, contacts_to_write, type=PREFIX_CONTACT, discard=False)
        write_output_file(output_file, contacts_to_discard, type=PREFIX_CONTACT, discard=True)
        with open(input_file, 'r', encoding=SOURCE_ENCODING) as ifile:
            print('{} - Required fields: {}'.format(PREFIX_CAMPANAS_CONSULTORA, I_FIELDS_CAMPANAS_CONSULTORA))
            reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
            campanas_consultoras_to_write, campanas_consultoras_to_discard = generate_campanas_consultoras(reader, contacts_to_write)
        output_file = os.path.join(output_folder, PREFIX_CAMPANAS_CONSULTORA + '_' + source_file)
        write_output_file(output_file, campanas_consultoras_to_write, type=PREFIX_CAMPANAS_CONSULTORA, discard=False)
        write_output_file(output_file, campanas_consultoras_to_discard, type=PREFIX_CAMPANAS_CONSULTORA, discard=True)
    except ValueError as ve:
        print(ve)
        raise ve


def import_from_csv_to_odata(source_folder, source_file, output_folder):
    try:
        input_file = os.path.join(source_folder, source_file)
        print('GENERAL - Opening input file: {}'.format(input_file))
        with open(input_file, 'r', encoding=SOURCE_ENCODING) as ifile:
            print('{} - Required fields: {}'.format(PREFIX_CONTACT, I_FIELDS_CONTACT))
            reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
            contacts_to_write, contacts_to_discard = generate_contacts(reader)
        output_file = os.path.join(output_folder, PREFIX_CONTACT + '_' + source_file)
        write_output_file(output_file, contacts_to_write, type=PREFIX_CONTACT, discard=False)
        write_output_file(output_file, contacts_to_discard, type=PREFIX_CONTACT, discard=True)
        with open(input_file, 'r', encoding=SOURCE_ENCODING) as ifile:
            print('{} - Required fields: {}'.format(PREFIX_CAMPANAS_CONSULTORA, I_FIELDS_CAMPANAS_CONSULTORA))
            reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
            campanas_consultoras_to_write, campanas_consultoras_to_discard = generate_campanas_consultoras(reader, contacts_to_write)
        output_file = os.path.join(output_folder, PREFIX_CAMPANAS_CONSULTORA + '_' + source_file)
        write_output_file(output_file, campanas_consultoras_to_write, type=PREFIX_CAMPANAS_CONSULTORA, discard=False)
        write_output_file(output_file, campanas_consultoras_to_discard, type=PREFIX_CAMPANAS_CONSULTORA, discard=True)
        # Invocación al servicio OData
        odata_access = ODataAccess()
        business_objects = {
            "Contacts": contacts_to_write
        }
        custom_business_objects = {
            "CampanasConsultora": campanas_consultoras_to_write
        }
        odata_access.post_data(business_objects, custom_business_objects)
    except ValueError as ve:
        print(ve)
        raise ve


def import_sql(output_folder):
    try:
        print('GENERAL - Connecting to DB {} on server {}'.format(SQL_DB, SQL_SERVER))
        sql_access = SqlServerAccess()
        conn = sql_access.connect()
        cursor = conn.cursor()
        cursor.execute(VIRTUAL_COACH_CONSULTORAS_QUERY)
        columns = [column[0] for column in cursor.description]
        query_result = []
        for row in cursor.fetchall():
            query_result.append(dict(zip(columns, row)))

        print('{} - Required fields: {}'.format(PREFIX_CONTACT, I_FIELDS_CONTACT))
        contacts_to_write, contacts_to_discard = generate_contacts(query_result)
        output_file = os.path.join(output_folder, + PREFIX_CONTACT + '_' + SQL_DB + '_' + \
                      datetime.strftime(datetime.utcnow(), '%Y%m%d_%H%M') + '.csv')
        write_output_file(output_file, contacts_to_write, type=PREFIX_CONTACT, discard=False)
        write_output_file(output_file, contacts_to_discard, type=PREFIX_CONTACT, discard=True)

        print('{} - Required fields: {}'.format(PREFIX_CAMPANAS_CONSULTORA, I_FIELDS_CAMPANAS_CONSULTORA))
        campanas_consultoras_to_write, campanas_consultoras_to_discard = generate_campanas_consultoras(query_result, contacts_to_write)
        output_file = os.path.join(output_folder, PREFIX_CAMPANAS_CONSULTORA + '_' + SQL_DB + '_' + \
                      datetime.strftime(datetime.utcnow(), '%Y%m%d_%H%M') + '.csv')
        write_output_file(output_file, campanas_consultoras_to_write, type=PREFIX_CAMPANAS_CONSULTORA, discard=False)
        write_output_file(output_file, campanas_consultoras_to_discard, type=PREFIX_CAMPANAS_CONSULTORA, discard=True)
    except ValueError as ve:
        print(ve)
        raise ve


# def main():
# if _name_ == "_main_":
# import_csv(SOURCE_FOLDER, SOURCE_FILE, OUTPUT_FOLDER)
#import_sql(OUTPUT_FOLDER)
import_from_csv_to_odata(SOURCE_FOLDER, SOURCE_FILE, OUTPUT_FOLDER)
