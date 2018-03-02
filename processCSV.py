# -*- coding: utf-8 -*-
import csv
import math
import decimal
from datetime import datetime
from settings import *
import re
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import settings


def format_date(attribute, row):
    try:
        date = datetime.strftime(datetime.strptime(row[attribute], '%d/%m/%Y'), '%Y%m%d')
        return date
    except ValueError:
        msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid for row {}'.format(attribute, row[attribute],
                                                                                  row.items())
        raise Exception(msg)


def format_float(attribute, row, min=None, max=None):
    try:
        float_number = decimal.Decimal(row[attribute])
        if (min is not None and float_number < min) or \
                (max is not None and float_number > max):
            msg = 'INPUT ERROR - Attribute "{}" value "{}" out of range for row {}'.format(attribute,
                                                                                           row[attribute],
                                                                                           row.items())
            raise Exception(msg)
        else:
            return '{:.10f}'.format(float_number)
    except ValueError:
        msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid for row {}'.format(attribute, row[attribute],
                                                                                  row.items())
        raise Exception(msg)


def format_text(text_string):
    return text_string.replace('NULL', '').strip()


def format_int(attribute, row, range):
    int_number = int(row[attribute])
    if int_number not in range:
        msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(attribute, row[attribute],
                                                                                         row.items())
        raise Exception(msg)
    else:
        return int_number


def format_phone(text_string):
    if text_string != '':
        return '+' + text_string
    else:
        return text_string


def generate_extended_info(input_file, output_file, origin='SAP_ODATA_IMPORT'):
    to_write = {}
    print('Processing input file: {}'.format(input_file))
    print('Required fields: {}'.format(I_FIELDS_USU_CAMP))
    read_counter = 0
    try:
        with open(input_file, 'r') as input_file:
            reader = csv.DictReader(input_file, delimiter=';')
            for row in reader:
                campana_usuario = {}
                for key in I_FIELDS_USU_CAMP:
                    if key not in row.keys():
                        msg = 'INPUT ERROR - Attribute "{}" is not included in the input file for row {}'.format(key,
                                                                                                                 row.items())
                        raise Exception(msg)

                ## CUSTOM VALIDATIONS
                campana_usuario[O_COD_PAIS] = row[I_COD_PAIS]
                if len(campana_usuario[O_COD_PAIS]) != 2:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_COD_PAIS,
                                                                                                     campana_usuario[
                                                                                                         O_COD_PAIS],
                                                                                                     row.items())
                    raise Exception(msg)
                campana_usuario[O_COD_REGION] = row[I_COD_REGION]
                if len(str(campana_usuario[O_COD_REGION])) > 3:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_COD_REGION,
                                                                                                     campana_usuario[
                                                                                                         O_COD_REGION],
                                                                                                     row.items())
                    raise Exception(msg)
                campana_usuario[O_COD_ZONA] = int(row[I_COD_ZONA])
                if len(str(campana_usuario[O_COD_ZONA])) > 4:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_COD_ZONA,
                                                                                                     campana_usuario[
                                                                                                         O_COD_ZONA],
                                                                                                     row.items())
                    raise Exception(msg)
                campana_usuario[O_COD_EBELISTA] = int(row[I_COD_EBELISTA])
                if len(str(campana_usuario[O_COD_EBELISTA])) > 15:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_COD_EBELISTA,
                                                                                                     campana_usuario[
                                                                                                         O_COD_EBELISTA],
                                                                                                     row.items())
                    raise Exception(msg)
                campana_usuario[O_EDAD_BELCORP] = int(row[I_EDAD_BELCORP])
                if len(str(campana_usuario[O_EDAD_BELCORP])) > 4:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_EDAD_BELCORP,
                                                                                                     campana_usuario[
                                                                                                         O_EDAD_BELCORP],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_COD_COMPORTAMIENTO] = int(row[I_COD_COMPORTAMIENTO])
                if campana_usuario[O_COD_COMPORTAMIENTO] not in range(0, 8):
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_COD_COMPORTAMIENTO,
                        campana_usuario[
                            O_COD_COMPORTAMIENTO],
                        row.items())
                    raise Exception(msg)

                campana_usuario[O_DESC_SEGMENTO] = row[I_DESC_SEGMENTO]
                if campana_usuario[O_DESC_SEGMENTO] not in [x[1] for x in D_SEGMENTOS]:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_DESC_SEGMENTO,
                                                                                                     campana_usuario[
                                                                                                         O_DESC_SEGMENTO],
                                                                                                     row.items())
                    raise Exception(msg)
                else:
                    if [campana_usuario[O_COD_COMPORTAMIENTO], campana_usuario[O_DESC_SEGMENTO]] not in D_SEGMENTOS:
                        msg = 'INPUT ERROR - Attributes "{}"-{} value "{}-{}" invalid tuple for row {}'.format(
                            O_COD_COMPORTAMIENTO,
                            O_DESC_SEGMENTO,
                            campana_usuario[
                                O_COD_COMPORTAMIENTO],
                            campana_usuario[
                                O_DESC_SEGMENTO],
                            row.items())
                        raise Exception(msg)

                campana_usuario[O_TIPO_CONSULTORA] = row[I_TIPO_CONSULTORA]
                if campana_usuario[O_TIPO_CONSULTORA] not in D_TIPO_CONSULTORA:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_TIPO_CONSULTORA,
                                                                                                     campana_usuario[
                                                                                                         O_TIPO_CONSULTORA],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_DESC_CONSTANCIA_NUEVAS] = row[I_DESC_CONSTANCIA_NUEVAS]
                # if campana_usuario[O_DESC_CONSTANCIA_NUEVAS] == '0':
                #     campana_usuario[O_DESC_CONSTANCIA_NUEVAS] = ''
                if campana_usuario[O_DESC_CONSTANCIA_NUEVAS] != '' and \
                                campana_usuario[O_DESC_CONSTANCIA_NUEVAS] not in D_CONSTANCIA_NUEVAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_DESC_CONSTANCIA_NUEVAS,
                        campana_usuario[
                            O_DESC_CONSTANCIA_NUEVAS],
                        row.items())
                    raise Exception(msg)

                campana_usuario[O_MARCA_LANZAMIENTO] = format_text(row[I_MARCA_LANZAMIENTO])
                if campana_usuario[O_MARCA_LANZAMIENTO] != '' and \
                                campana_usuario[O_MARCA_LANZAMIENTO] not in D_MARCAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_MARCA_LANZAMIENTO,
                        campana_usuario[
                            O_MARCA_LANZAMIENTO],
                        row.items())
                    raise Exception(msg)

                campana_usuario[O_MARCA_TOP] = format_text(row[I_MARCA_TOP])
                if campana_usuario[O_MARCA_TOP] != '' and \
                                campana_usuario[O_MARCA_TOP] not in D_MARCAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_MARCA_TOP,
                                                                                                     campana_usuario[
                                                                                                         O_MARCA_TOP],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_CAT_LANZAMIENTO] = format_text(row[I_CAT_LANZAMIENTO])
                if campana_usuario[O_CAT_LANZAMIENTO] != '' and \
                                campana_usuario[O_CAT_LANZAMIENTO] not in D_CATEGORIAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_CAT_LANZAMIENTO,
                                                                                                     campana_usuario[
                                                                                                         O_CAT_LANZAMIENTO],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_CAT_TOP] = format_text(row[I_CAT_TOP])
                if campana_usuario[O_CAT_TOP] != '' and \
                                campana_usuario[O_CAT_TOP] not in D_CATEGORIAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_CAT_TOP,
                                                                                                     campana_usuario[
                                                                                                         O_CAT_TOP],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_COD_VTA_LANZAMIENTO] = format_text(row[I_COD_VTA_LANZAMIENTO])
                if len(campana_usuario[O_COD_VTA_LANZAMIENTO]) not in range(0, 6):
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_COD_VTA_LANZAMIENTO,
                        campana_usuario[
                            O_COD_VTA_LANZAMIENTO],
                        row.items())
                    raise Exception(msg)

                campana_usuario[O_COD_VTA_TOP] = format_text(row[I_COD_VTA_TOP])
                if len(campana_usuario[O_COD_VTA_TOP]) not in range(0, 6):
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_COD_VTA_TOP,
                                                                                                     campana_usuario[
                                                                                                         O_COD_VTA_TOP],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_DESC_MARCA_SCORE] = format_text(row[I_DESC_MARCA_SCORE])
                if campana_usuario[O_DESC_MARCA_SCORE] == '0':
                    campana_usuario[O_DESC_MARCA_SCORE] = ''
                if campana_usuario[O_DESC_MARCA_SCORE] != '' and \
                                campana_usuario[O_DESC_MARCA_SCORE] not in D_MARCAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_DESC_MARCA_SCORE,
                                                                                                     campana_usuario[
                                                                                                         O_DESC_MARCA_SCORE],
                                                                                                     row.items())
                    raise Exception(msg)

                campana_usuario[O_DESC_CAT_SCORE] = format_text(row[I_DESC_CAT_SCORE])
                if campana_usuario[O_DESC_CAT_SCORE] == '0':
                    campana_usuario[O_DESC_CAT_SCORE] = ''
                if campana_usuario[O_DESC_CAT_SCORE] != '' and \
                                campana_usuario[O_DESC_CAT_SCORE] not in D_CATEGORIAS:
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(O_DESC_CAT_SCORE,
                                                                                                     campana_usuario[
                                                                                                         O_DESC_CAT_SCORE],
                                                                                                     row.items())
                    raise Exception(msg)

                ## TEXTS
                campana_usuario[O_CUC_LANZAMIENTO] = format_text(row[I_CUC_LANZAMIENTO])
                campana_usuario[O_CUC_TOP] = format_text(row[I_CUC_TOP])
                campana_usuario[O_DESC_LANZAMIENTO] = format_text(row[I_DESC_LANZAMIENTO])
                campana_usuario[O_LINK_LANZAMIENTO] = format_text(row[I_LINK_LANZAMIENTO])
                campana_usuario[O_DESC_TOP] = format_text(row[I_DESC_TOP])
                campana_usuario[O_LINK_TOP] = format_text(row[I_LINK_TOP])
                campana_usuario[O_INVITACION_SMS_FICHA] = format_text(row[I_INVITACION_SMS_FICHA])
                campana_usuario[O_INVITACION_SMS_LANDING] = format_text(row[I_INVITACION_SMS_LANDING])
                campana_usuario[O_INVITACION_EMAIL_FICHA] = format_text(row[I_INVITACION_EMAIL_FICHA])
                campana_usuario[O_INVITACION_EMAIL_LANDING] = format_text(row[I_INVITACION_EMAIL_LANDING])
                campana_usuario[O_LINK_OFERTAS] = format_text(row[I_LINK_OFERTAS])

                ## FLOATS
                campana_usuario[O_SCORE_MARCA] = format_float(I_SCORE_MARCA, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_CATEGORIA] = format_float(I_SCORE_CATEGORIA, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_TOP] = format_float(I_SCORE_TOP, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_LANZAMIENTO] = format_float(I_SCORE_LANZAMIENTO, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_VISITAS] = format_float(I_SCORE_VISITAS, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_TIP_GESTION_DIGITAL] = format_float(I_SCORE_TIP_GESTION_DIGITAL, row, min=0.0,
                                                                            max=1.0)
                campana_usuario[O_SCORE_TIP_COBRANZA] = format_float(I_SCORE_TIP_COBRANZA, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_MAS_CLIENTES] = format_float(I_SCORE_MAS_CLIENTES, row, min=0.0, max=1.0)
                campana_usuario[O_SCORE_TIP_PEDIDO_ONLINE] = format_float(I_SCORE_TIP_PEDIDO_ONLINE, row)
                campana_usuario[O_PROBABILIDAD_FUGA] = format_float(I_PROBABILIDAD_FUGA, row, min=0.0, max=100.0)
                campana_usuario[O_VTA_FACTURADA_UC] = format_float(I_VTA_FACTURADA_UC, row)
                campana_usuario[O_PRECIO_LANZAMIENTO] = format_float(I_PRECIO_LANZAMIENTO, row)
                campana_usuario[O_PRECIO_TOP] = format_float(I_PRECIO_TOP, row)

                ## INTEGERS
                campana_usuario[O_ANIO_CAMPANA_EXPOSICION] = int(row[I_ANIO_CAMPANA_EXPOSICION][0:4])
                campana_usuario[O_NRO_CAMPANA_EXPOSICION] = int(row[I_ANIO_CAMPANA_EXPOSICION][4:6])
                if campana_usuario[O_NRO_CAMPANA_EXPOSICION] not in range(1, 19):
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_NRO_CAMPANA_EXPOSICION,
                        row[O_NRO_CAMPANA_EXPOSICION],
                        row.items())
                    raise Exception(msg)
                campana_usuario[O_ANIO_CAMPANA_INGRESO] = int(row[I_ANIO_CAMPANA_INGRESO][0:4])
                campana_usuario[O_NRO_CAMPANA_INGRESO] = int(row[I_ANIO_CAMPANA_INGRESO][4:6])
                if campana_usuario[O_NRO_CAMPANA_INGRESO] not in range(1, 19):
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_NRO_CAMPANA_INGRESO,
                        row[O_NRO_CAMPANA_INGRESO],
                        row.items())
                    raise Exception(msg)
                campana_usuario[O_ANIO_CAMPANA_PROCESO] = int(row[I_ANIO_CAMPANA_PROCESO][0:4])
                campana_usuario[O_NRO_CAMPANA_PROCESO] = int(row[I_ANIO_CAMPANA_PROCESO][4:6])
                if campana_usuario[O_NRO_CAMPANA_PROCESO] not in range(1, 19):
                    msg = 'INPUT ERROR - Attribute "{}" value "{}" invalid domain for row {}'.format(
                        O_NRO_CAMPANA_PROCESO,
                        row[O_NRO_CAMPANA_PROCESO],
                        row.items())
                    raise Exception(msg)
                campana_usuario[O_NRO_CAMPANA_NUEVAS] = format_int(I_NRO_CAMPANA_NUEVAS, row, range(0, 7))
                campana_usuario[O_NRO_PEDIDOS_NUEVAS] = format_int(I_NRO_PEDIDOS_NUEVAS, row, range(0, 7))
                campana_usuario[O_IP_UNICO_PU5C] = format_int(I_IP_UNICO_PU5C, row, range(0, 6))
                campana_usuario[O_OFERTA_DIGITAL_PU5C] = format_int(I_OFERTA_DIGITAL_PU5C, row, range(0, 7))
                campana_usuario[O_MONTO_DEUDA] = int(row[I_MONTO_DEUDA])
                campana_usuario[O_MAX_VTA_FACTURADA_PU5C] = int(float(row[I_MAX_VTA_FACTURADA_PU5C]))

                ## DATES
                campana_usuario[O_FECHA_INICIO_VENTA] = format_date(I_FECHA_INICIO_VENTA, row)
                campana_usuario[O_FECHA_FIN_VENTA] = format_date(I_FECHA_FIN_VENTA, row)
                campana_usuario[O_FECHA_INICIO_FACTURACION] = format_date(I_FECHA_INICIO_FACTURACION, row)
                campana_usuario[O_FECHA_FIN_FACTURACION] = format_date(I_FECHA_FIN_FACTURACION, row)
                campana_usuario[O_FECHA_ENVIO] = format_date(I_FECHA_ENVIO, row)

                ## FLAGS
                campana_usuario[O_FLAG_CONSTANCIA_NUEVAS] = format_int(I_FLAG_CONSTANCIA_NUEVAS, row, range(-1, 2))
                campana_usuario[O_FLAG_TP1] = format_int(I_FLAG_TP1, row, range(-1, 2))
                campana_usuario[O_FLAG_TP2] = format_int(I_FLAG_TP2, row, range(-1, 2))
                campana_usuario[O_FLAG_IP_UNICO] = format_int(I_FLAG_IP_UNICO, row, range(0, 2))
                campana_usuario[O_FLAG_PASO_PEDIDO_CACT] = format_int(I_FLAG_PASO_PEDIDO_CACT, row, range(0, 2))
                campana_usuario[O_FLAG_DEUDA] = format_int(I_FLAG_DEUDA, row, range(0, 2))
                campana_usuario[O_FLAG_CORREO] = format_int(I_FLAG_CORREO, row, range(0, 2))
                campana_usuario[O_FLAG_CELULAR] = format_int(I_FLAG_CELULAR, row, range(0, 2))
                campana_usuario[O_FLAG_INSCRITA] = format_int(I_FLAG_INSCRITA, row, range(0, 2))
                campana_usuario[O_FLAG_OFERTA_DIGITAL_UC] = format_int(I_FLAG_OFERTA_DIGITAL_UC, row, range(0, 2))
                campana_usuario[O_FLAG_PASO_PEDIDO] = format_int(I_FLAG_PASO_PEDIDO, row, range(0, 2))
                campana_usuario[O_FLAG_INSCRITA_GANA_MAS] = format_int(I_FLAG_INSCRITA_GANA_MAS, row, range(0, 2))

                campana_usuario[O_ID_CAMPANA_CONSULTORA] = str(campana_usuario[O_ANIO_CAMPANA_EXPOSICION]) + \
                                                           str(campana_usuario[O_NRO_CAMPANA_EXPOSICION]) + '_' + \
                                                           str(campana_usuario[O_COD_EBELISTA])
                campana_usuario[O_IDORIGIN] = origin
                to_write[campana_usuario[O_ID_CAMPANA_CONSULTORA]] = campana_usuario
                read_counter += 1

        print('Lines read: {}'.format(read_counter))
        print('Output fields: {}'.format(O_FIELDS_USU_CAMP))
        write_counter = 0
        batch_size = BATCH_SIZE
        max_files = math.ceil(len(to_write.values()) / batch_size)
        to_write_values = list(to_write.values())
        for file_number in range(max_files):
            parcial_output_file = output_file.replace('.csv', '_{}.csv'.format(file_number))
            print('Processing output file: {}'.format(parcial_output_file))
            with open(parcial_output_file, 'w') as ofile:
                writer = csv.DictWriter(ofile, fieldnames=O_FIELDS_USU_CAMP, lineterminator='\n', delimiter=';')
                ofile.write(O_CAMPANAS_CONSULTORAS_FILE_HEADER)
                writer.writeheader()
                ini_index = file_number * batch_size
                end_index = min((file_number + 1) * batch_size, len(to_write_values))
                for item in to_write_values[ini_index:end_index]:
                    writer.writerow(item)
                    write_counter += 1
        print('Lines written: {}'.format(write_counter))
    except ValueError as ve:
        print(ve)
        print(row)
        raise


def generate_contact(input_file, output_file, origin='SAP_ODATA_IMPORT'):
    try:
        to_write = {}
        to_discard = {}
        to_write_odata = []
        to_discard_odata = []
        print('Processing input file: {}'.format(input_file))
        print('Required fields: {}'.format(I_FIELDS_CONTACT))
        read_counter = 0
        with open(input_file, 'r') as input_file:
            reader = csv.DictReader(input_file, delimiter=';')
            timestamp = get_timestamp_str()
            for row in reader:
                contact = {}
                for key in I_FIELDS_CONTACT:
                    if key not in row.keys():
                        msg = 'INPUT ERROR - Attribute "{}" is not included in the input file for row {}'.format(key,
                                                                                                                 row.items())
                        raise Exception(msg)
                contact[O_ID] = int(row[I_COD_EBELISTA])
                contact[O_NAME_FIRST] = format_text(row[I_PRIMER_NOMBRE])
                contact[O_NAME_LAST] = format_text(row[I_APE_PATERNO])
                contact[O_COUNTRY_FT] = format_text(row[I_DESC_PAIS])
                if MODE == 'PRODUCTIVE':
                    contact[O_SMTP_ADDR] = row[I_CORREO_ELECTRONICO]
                    contact[O_TELNR_MOBILE] = format_phone(row[I_TEL_MOVIL])
                else:
                    contact[O_SMTP_ADDR] = 'brunoo.gonzalez+{}@gmail.com'.format(read_counter + 1)
                contact[O_DATE_OF_BIRTH] = format_date(I_FECHA_NACIMIENTO, row)
                contact[O_CODIGOEBELISTA] = int(row[I_COD_EBELISTA])
                contact[O_DOCIDENTIDAD] = format_text(row[I_DOC_IDENTIDAD])
                contact[O_ID_ORIGIN] = origin
                for key in O_FIELDS_CONTACT:
                    if key not in contact.keys():
                        contact[key] = ''
                # Copia de diccionario de contacto y edición de claves
                contact_odata = contact.copy()
                for contact_field in CONTACT_FIELDS:
                    # Si existe la clave destino: cambio de nombre de clave
                    try:
                        # Chequea que tenga un valor diferente de vacío
                        if contact_odata[getattr(settings, 'O_{}'.format(contact_field))] != '':
                            value = contact_odata.pop(getattr(settings, 'O_{}'.format(contact_field)))
                            # Modificaciones a atributos por cambio de tipo de dato
                            if contact_field in ['ID', 'CODIGOEBELISTA']:
                                # Modificación de int a str
                                value = str(value)
                            elif contact_field in ['DATE_OF_BIRTH']:
                                # Modificación de fecha
                                value = '/Date({})/'.format(value)
                            contact_odata[getattr(settings, 'S_{}'.format(contact_field))] = value
                        else:
                            del contact_odata[getattr(settings, 'O_{}'.format(contact_field))]
                    except:
                        # Si no existe la clave destino: elimino clave y valor de origen
                        try:
                            del contact_odata[getattr(settings, 'O_{}'.format(contact_field))]
                        except:
                            pass
                # Agregado de Timestamp para servicio
                contact_odata['Timestamp'] = timestamp
                match_phone = re.search(PHONE_REGEX, contact[O_TELNR_MOBILE])
                match_mail = re.search(MAIL_REGEX, contact[O_SMTP_ADDR])
                if (match_phone or contact[O_TELNR_MOBILE] == '') and \
                        (match_mail or contact[O_SMTP_ADDR] == ''):
                    to_write[contact[O_ID]] = contact
                    to_write_odata.append(contact_odata)
                else:
                    to_discard[contact[O_ID]] = contact
                    to_discard_odata.append(contact_odata)
                read_counter += 1

            print('Lines read: {}'.format(read_counter))
            print('Processing output file: {}'.format(output_file))
            print('Output fields: {}'.format(O_FIELDS_CONTACT))

            if OUTPUT_MODE == 'ODATA':
                # Invocación de servicio en batch
                last_index = 0
                odata_results = []
                while last_index < len(to_write_odata):
                    result = post_odata_contacts(to_write_odata[last_index:last_index + BATCH_SIZE])
                    if result != 'OK':
                        odata_results.append(result + [last_index, last_index + BATCH_SIZE])
                    else:
                        odata_results.append(['POST_ODATA', 201, last_index, last_index + BATCH_SIZE])
                    last_index += BATCH_SIZE
                with open(output_file.replace('.csv', '_ODATA_RESULTS.csv'), 'w') as ofile:
                    writer = csv.writer(ofile, delimiter=';')
                    writer.writerow(['operation', 'status_code', 'index_from', 'index_to'])
                    writer.writerows(odata_results)
            elif OUTPUT_MODE == 'FILE':
                write_counter = 0
                batch_size = BATCH_SIZE
                max_files = math.ceil(len(to_write.values()) / batch_size)
                to_write_values = list(to_write.values())
                for file_number in range(max_files):
                    parcial_output_file = output_file.replace('.csv', '_{}.csv'.format(file_number))
                    print('Processing output file: {}'.format(parcial_output_file))
                    with open(parcial_output_file, 'w') as ofile:
                        ofile.write(O_CONTACT_FILE_HEADER)
                        writer = csv.DictWriter(ofile, fieldnames=O_FIELDS_CONTACT, lineterminator='\n', delimiter=';')
                        writer.writeheader()
                        ini_index = file_number * batch_size
                        end_index = min((file_number + 1) * batch_size, len(to_write_values))
                        for item in to_write_values[ini_index:end_index]:
                            writer.writerow(item)
                            write_counter += 1
                print('Lines written: {}'.format(write_counter))

                discard_counter = 0
                with open(output_file.replace('.csv', '_DISCARDED.csv'), 'w') as ofile:
                    ofile.write(O_CONTACT_FILE_HEADER)
                    writer = csv.DictWriter(ofile, fieldnames=O_FIELDS_CONTACT, lineterminator='\n', delimiter=';')
                    writer.writeheader()
                    for item in to_discard.values():
                        writer.writerow(item)
                        discard_counter += 1
                print('Lines discarded: {}'.format(discard_counter))
            else:
                pass
    except ValueError as ve:
        print(ve)
        print(row)
        raise


def generate_interaction(input_file, output_file):
    try:
        to_write = {}
        to_discard = {}
        print('Processing input file: {}'.format(input_file))
        print('Required fields: {}'.format(I_FIELDS_INTERACT))
        read_counter = 0
        with open(input_file, 'r') as input_file:
            reader = csv.DictReader(input_file, delimiter=';')
            for row in reader:
                interaction = {}
                for key in I_FIELDS_INTERACT:
                    if key not in row.keys():
                        msg = 'INPUT ERROR - Attribute "{}" is not included in the input file for row {}'.format(key,
                                                                                                                 row.items())
                        raise Exception(msg)
                if row[I_TEL_MOVIL] != '':
                    interaction[O_ID_ORIGIN] = 'MOBILE_APP_TOKEN'
                    interaction[O_ID] = format_text(row[I_APP_TOKEN])
                    interaction[O_COMM_MEDIUM] = 'MOBILE_APP'
                    interaction[O_IA_TYPE] = 'MOB_APP_INSTALLED'
                    # Timestamp without timezone
                    interaction[O_TIMESTAMP] = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S')
                    interaction[O_DEVICE_TYPE] = 'PHONE'
                    interaction[O_NAME_FIRST] = format_text(row[I_PRIMER_NOMBRE])
                    interaction[O_NAME_LAST] = format_text(row[I_APE_PATERNO])
                    interaction[O_TELNR_MOBILE] = format_phone(row[I_TEL_MOVIL])
                    for key in O_FIELDS_INTERACTION:
                        if key not in interaction.keys():
                            interaction[key] = ''

                    match_phone = re.search(PHONE_REGEX, interaction[O_TELNR_MOBILE])
                    if match_phone:
                        to_write[str(interaction[O_NAME_FIRST]) + '_' +
                                 str(interaction[O_NAME_LAST]) + '_' +
                                 str(interaction[O_TELNR_MOBILE])] = interaction
                    else:
                        to_discard[str(interaction[O_NAME_FIRST]) + '_' +
                                   str(interaction[O_NAME_LAST]) + '_' +
                                   str(interaction[O_TELNR_MOBILE])] = interaction

                read_counter += 1

            print('Lines read: {}'.format(read_counter))
            print('Processing output file: {}'.format(output_file))
            print('Output fields: {}'.format(O_FIELDS_INTERACTION))

            write_counter = 0
            if MODE == 'PRODUCTIVE':
                batch_size = BATCH_SIZE
                max_files = math.ceil(len(to_write.values()) / batch_size)
                to_write_values = list(to_write.values())
                for file_number in range(max_files):
                    parcial_output_file = output_file.replace('.csv', '_{}.csv'.format(file_number))
                    print('Processing output file: {}'.format(parcial_output_file))
                    with open(parcial_output_file, 'w') as ofile:
                        ofile.write(O_INTERACTION_FILE_HEADER)
                        writer = csv.DictWriter(ofile, fieldnames=O_FIELDS_INTERACTION, lineterminator='\n',
                                                delimiter=';')
                        writer.writeheader()
                        ini_index = file_number * batch_size
                        end_index = min((file_number + 1) * batch_size, len(to_write_values))
                        for item in to_write_values[ini_index:end_index]:
                            writer.writerow(item)
                            write_counter += 1
            print('Lines written: {}'.format(write_counter))

            discard_counter = 0
            if MODE == 'PRODUCTIVE':
                with open(output_file.replace('.csv', '_DISCARDED.csv'), 'w') as ofile:
                    ofile.write(O_INTERACTION_FILE_HEADER)
                    writer = csv.DictWriter(ofile, fieldnames=O_FIELDS_INTERACTION, lineterminator='\n', delimiter=';')
                    writer.writeheader()
                    for item in to_discard.values():
                        writer.writerow(item)
                        discard_counter += 1
            print('Lines discarded: {}'.format(discard_counter))
    except ValueError as ve:
        print(ve)
        print(row)
        raise


# Obtiene el timestamp actual y trunca la cantidad de caracteres, reemplazando el . que está de más
def get_timestamp_str():
    return '/Date({})/'.format(str(round(time.time(), 3)).replace('.', ''))


def post_odata_contacts(contacts_data):
    headers = {
        'x-csrf-token': 'Fetch',
        'cache-control': 'no-cache'
    }
    session = requests.session()
    response = session.get(ODATA_GET_CSRF_URL,
                           headers=headers,
                           auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD))
    if response.status_code == 200:
        headers = {
            'x-csrf-token': response.headers['x-csrf-token'],
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }
        post_data = {
            "Id": "",
            "Timestamp": get_timestamp_str(),
            "UserName": "INTEGRATION",
            "SourceSystemType": "EXT",
            "SourceSystemId": "ODATA",
            "Contacts": contacts_data
        }
        response = session.post(ODATA_POST_IMPORT_HEADERS_URL,
                                headers=headers,
                                auth=HTTPBasicAuth(ODATA_USER, ODATA_PASSWORD),
                                data=json.dumps(post_data))
        if response.status_code == 201:
            return 'OK'
        else:
            return ['POST_ODATA', response.status_code]
    else:
        return ['GET_CSRF_TOKEN', response.status_code]


# generate_extended_info('{}/{}'.format(SOURCE_FOLDER, SOURCE_FILE),
#                        '{}/CAMPANAS_CONSULTORAS_{}'.format(OUTPUT_FOLDER, SOURCE_FILE))
generate_contact('{}/{}'.format(SOURCE_FOLDER, SOURCE_FILE),
                 '{}/CONTACTS_{}'.format(OUTPUT_FOLDER, SOURCE_FILE))
# generate_interaction('{}/{}'.format(SOURCE_FOLDER, SOURCE_FILE),
#                      '{}/INTERACTIONS_{}'.format(OUTPUT_FOLDER, SOURCE_FILE))
