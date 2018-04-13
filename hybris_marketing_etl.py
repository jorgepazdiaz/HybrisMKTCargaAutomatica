# -*- coding: utf-8 -*-
import csv
import math
import decimal
import re
import os
import json
import logging
import logging.handlers
import argparse
from datetime import datetime
from common.settings import *
from common.messages import *
from common.domains import D_MARCAS, D_CATEGORIAS, D_CONSTANCIA_NUEVAS, D_TIPO_CONSULTORA, D_SEGMENTOS
from mapping.contacts import *
from mapping.campanas_consultoras import *
from mapping.interactions import *
from validate_email import validate_email
from dal.dal import SqlServerAccess, ODataAccess
from dal.queries.virtual_coach_consultoras import VIRTUAL_COACH_CONSULTORAS_QUERY
from dal.conn_credentials import ODATA_CONTACT, ODATA_INTERACTION, ODATA_CAMPANA_CONSULTORA


def format_date(attribute, row):
    try:
        date = datetime.strftime(datetime.strptime(str(row[attribute]), '%Y%m%d'), '%Y%m%d')
        return date
    except ValueError:
        raise Exception(MSG_INVALID_TYPE.format(attribute))


def format_decimal(attribute, row, minimum=None, maximum=None):
    try:
        float_number = decimal.Decimal(row[attribute])
        if (minimum is not None and float_number < minimum) or \
                (maximum is not None and float_number > maximum):
            raise Exception(MSG_OUT_OF_RANGE.format(attribute, minimum, maximum))
        else:
            return '{:.10f}'.format(float_number)
    except ValueError:
        raise Exception(MSG_INVALID_TYPE.format(attribute))


def format_int(attribute, row, num_range):
    try:
        int_number = int(row[attribute])
        if int_number not in num_range:
            raise Exception(MSG_OUT_OF_RANGE.format(attribute, min(list(num_range)), max(list(num_range))))
        else:
            return int_number
    except ValueError:
        raise Exception(MSG_INVALID_TYPE.format(attribute))


def format_text(attribute, row):
    try:
        return row[attribute].replace('NULL', '').strip()
    except ValueError:
        raise Exception(MSG_INVALID_TYPE.format(attribute))


def format_phone(attribute, row):
    try:
        phone_string = str(row[attribute]).strip()
        if phone_string != '':
            return '+' + phone_string
        else:
            raise MSG_EMPTY_PHONE
    except ValueError:
        raise Exception(MSG_INVALID_PHONE)


def generate_empty_attributes(item, fields):
    for key in fields:
        if key not in item.keys():
            item[key] = ''


def write_output_file(output_file, to_write, output_file_type, discard=False):
    logger = logging.getLogger('{}.write_output_file'.format(LOGGER_NAME))
    logger.debug('Writing file: {}'.format(output_file))
    if output_file_type not in OUTPUT_FILE_TYPES:
        msg = 'Function argument output file type with value "{}" is not included in \{{}\}'.format(output_file_type,
                                                                                                    OUTPUT_FILE_TYPES)
        logger.error(msg)
        raise Exception(msg)
    elif output_file_type == PREFIX_CONTACT:
        field_names = O_CONTACT_FIELDS
        file_header = O_CONTACT_FILE_HEADER
    elif output_file_type == PREFIX_INTERACTION:
        field_names = O_INTERACTION_FIELDS
        file_header = O_INTERACTION_FILE_HEADER
    elif output_file_type == PREFIX_CAMPANA_CONSULTORA:
        field_names = O_CAMPANA_CONSULTORA_FIELDS
        file_header = O_CAMPANA_CONSULTORA_FILE_HEADER
    if discard:
        logger.debug('{} - Writing discarded file: {}'.format(output_file_type, output_file))
        discard_counter = 0
        with open(output_file.replace('.csv', '_DISCARDED.csv'), 'w', encoding="utf8") as ofile:
            field_names.copy()
            field_names.append(O_DISCARD_MOTIVE)
            # ofile.write(file_header)
            writer = csv.DictWriter(ofile, fieldnames=field_names, lineterminator='\n', delimiter=';')
            writer.writeheader()
            for item in to_write.values():
                writer.writerow(item)
                discard_counter += 1
            ofile.flush()
            ofile.close()
        logger.info('{} - Lines discarded: {}'.format(output_file_type, discard_counter))
    else:
        logger.debug('{} - Writing output file(s): {}'.format(output_file_type, output_file))
        logger.debug('{} - Output fields: {}'.format(output_file_type, field_names))
        write_counter = 0
        max_files = int(math.ceil(len(to_write.values()) / BATCH_SIZE))
        if output_file_type == PREFIX_INTERACTION:
            to_write_values = []
            for it_1 in to_write.values():
                for it_2 in it_1:
                    to_write_values.append(it_2)
        else:
            to_write_values = list(to_write.values())
        for file_number in range(max_files):
            parcial_output_file = output_file.replace('.csv', '_{}.csv'.format(file_number))
            logger.debug('{} - Processing output file: {}'.format(output_file_type, parcial_output_file))
            with open(parcial_output_file, 'w', encoding='utf8') as ofile:
                ofile.write(file_header)
                writer = csv.DictWriter(ofile, fieldnames=field_names, lineterminator='\n', delimiter=';')
                writer.writeheader()
                ini_index = file_number * BATCH_SIZE
                end_index = min((file_number + 1) * BATCH_SIZE, len(to_write_values))
                for item in to_write_values[ini_index:end_index]:
                    writer.writerow(item)
                    write_counter += 1
                ofile.flush()
                ofile.close()
        logger.info('{} - Lines written: {}'.format(output_file_type, write_counter))


def generate_contacts(contacts):
    logger = logging.getLogger('{}.generate_contacts'.format(LOGGER_NAME))
    logger.debug('Processing input')
    logger.debug('Required fields: {}'.format(I_FIELDS_CONTACT))
    contacts_to_write = {}
    contacts_to_discard = {}
    read_counter = 0
    for row in contacts:
        contact = {}
        read_counter += 1
        try:
            for key in I_FIELDS_CONTACT:
                if key not in row.keys():
                    raise ValueError(MSG_INPUT_ERROR.format(key))
            contact[O_ID] = str(int(row[I_COD_EBELISTA])) + '_' + str(row[I_COD_PAIS])
            contact[O_NAME_FIRST] = format_text(I_PRIMER_NOMBRE, row)
            contact[O_NAME_LAST] = format_text(I_APE_PATERNO, row)
            contact[O_COUNTRY_FT] = format_text(I_DESC_PAIS, row)
            if MODE == 'PRODUCTIVE':
                contact[O_SMTP_ADDR] = str(row[I_CORREO_ELECTRONICO]).strip()
                # TODO: modificar cuando confirme que se realizarán los controles correspondientes en los datos fuente
                # contact[O_TELNR_MOBILE] = format_phone(I_TEL_MOVIL, row)
            else:
                contact[O_SMTP_ADDR] = TEST_MAIL.format(read_counter + 1)
                contact[O_TELNR_MOBILE] = format_phone(I_TEL_MOVIL, row)
            if row[I_FECHA_NACIMIENTO] != '':
                contact[O_DATE_OF_BIRTH] = format_date(I_FECHA_NACIMIENTO, row)
            # contact[O_CODIGOEBELISTA] = int(row[I_COD_EBELISTA])
            contact[O_CODIGOEBELISTA] = str(row[I_COD_EBELISTA]).strip()
            contact[O_DOCIDENTIDAD] = format_text(I_DOC_IDENTIDAD, row)
            contact[O_ID_ORIGIN] = 'SAP_ODATA_IMPORT'
            generate_empty_attributes(contact, O_CONTACT_FIELDS)

            # Email & phone Validation
            is_valid_phone = re.search(PHONE_REGEX, contact[O_TELNR_MOBILE])
            is_valid_mail = validate_email(contact[O_SMTP_ADDR])
            if contact[O_SMTP_ADDR] == '' and contact[O_TELNR_MOBILE] == '':
                raise ValueError(MSG_NO_CONTACT_INFO)
            elif contact[O_SMTP_ADDR] == '':
                raise ValueError(MSG_EMPTY_MAIL)
            elif contact[O_SMTP_ADDR] != '':
                if not is_valid_mail:
                    raise ValueError(MSG_INVALID_MAIL)
                else:
                    [local_part, domain_part] = str(contact[O_SMTP_ADDR]).split('@', 1)
                    if not re.search(LOCAL_PART_REGEX, local_part):
                        raise ValueError(MSG_INVALID_MAIL)
                    else:
                        contacts_to_write[contact[O_ID]] = contact
            elif not (is_valid_phone or contact[O_TELNR_MOBILE] == ''):
                raise ValueError(MSG_INVALID_PHONE)
            else:
                contacts_to_write[contact[O_ID]] = contact
        except Exception as e:
            discarded = contact.copy()
            discarded[O_DISCARD_MOTIVE] = e.args[0]
            if O_ID is not discarded.keys():
                contact[O_ID] = str(row[I_COD_EBELISTA]).strip() + '_' + str(row[I_COD_PAIS]).strip()
            if O_NAME_FIRST is not discarded.keys():
                contact[O_NAME_FIRST] = str(row[I_PRIMER_NOMBRE]).strip()
            if O_NAME_LAST is not discarded.keys():
                contact[O_NAME_LAST] = str(row[I_APE_PATERNO]).strip()
            if O_COUNTRY_FT is not discarded.keys():
                contact[O_COUNTRY_FT] = str(row[I_DESC_PAIS]).strip()
            if O_SMTP_ADDR is not discarded.keys():
                contact[O_SMTP_ADDR] = str(row[I_CORREO_ELECTRONICO]).strip()
            if O_TELNR_MOBILE is not discarded.keys():
                contact[O_TELNR_MOBILE] = str(row[I_TEL_MOVIL]).strip()
            if O_DATE_OF_BIRTH is not discarded.keys():
                contact[O_DATE_OF_BIRTH] = str(row[I_FECHA_NACIMIENTO]).strip()
            if O_CODIGOEBELISTA is not discarded.keys():
                contact[O_CODIGOEBELISTA] = str(row[I_COD_EBELISTA]).strip()
            if O_DOCIDENTIDAD is not discarded.keys():
                contact[O_DOCIDENTIDAD] = str(row[I_DOC_IDENTIDAD]).strip()
            if O_ID_ORIGIN is not discarded.keys():
                contact[O_ID_ORIGIN] = 'SAP_ODATA_IMPORT'
            generate_empty_attributes(discarded, O_CONTACT_FIELDS)
            contacts_to_discard[contact[O_ID]] = discarded
            for key in row.keys():
                row[key] = str(row[key])
            logger.error('Discarded {}: {}'.format(discarded[O_DISCARD_MOTIVE], json.dumps(row)))
    logger.info('Lines read: {} - To write: {} - Discarded: {}'.
                format(read_counter, len(contacts_to_write), len(contacts_to_discard)))
    return contacts_to_write, contacts_to_discard


def generate_interactions(interactions, contacts):
    logger = logging.getLogger('{}.generate_interactions'.format(LOGGER_NAME))
    logger.debug('Processing input')
    logger.debug('Required fields: {}'.format(I_FIELDS_APP_INSTALLED))
    interactions_to_write = {}
    interactions_to_discard = {}
    read_counter = 0
    for row in interactions:
        try:
            apps_installed = []
            read_counter += 1
            for key in I_FIELDS_APP_INSTALLED:
                if key not in row.keys():
                    raise Exception(MSG_INPUT_ERROR.format(key))
            # Chequea las aplicaciones instaladas
            if format_int(I_FLAG_APP_CONS, row, range(0, 2)) == 1:
                apps_installed.append(I_FLAG_APP_CONS)
            if format_int(I_FLAG_APP_SOCIA, row, range(0, 2)) == 1:
                apps_installed.append(I_FLAG_APP_SOCIA)
            contact_id = str(int(row[I_COD_EBELISTA])) + '_' + str(row[I_COD_PAIS])
            # Agrega una interacción por aplicación instalada
            for app in apps_installed:
                interaction = {}
                if app == I_FLAG_APP_CONS:
                    interaction[O_ID_ORIGIN] = APP_CONS_ID_ORIGIN
                    interaction[O_ID] = format_text(I_TOKEN_APP_CONS, row)
                elif app == I_FLAG_APP_SOCIA:
                    interaction[O_ID_ORIGIN] = APP_SOCIA_ID_ORIGIN
                    interaction[O_ID] = format_text(I_TOKEN_APP_SOCIA, row)
                interaction[O_COMM_MEDIUM] = 'MOBILE_APP'
                interaction[O_IA_TYPE] = 'MOB_APP_INSTALLED'
                interaction[O_DEVICE_TYPE] = 'PHONE'
                interaction[O_TIMESTAMP] = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S')
                interaction[O_NAME_FIRST] = format_text(I_PRIMER_NOMBRE, row)
                interaction[O_NAME_LAST] = format_text(I_APE_PATERNO, row)
                interaction[O_TELNR_MOBILE] = format_phone(I_TEL_MOVIL, row)
                logger.info('interaction[O_TELNR_MOBILE]: {}'.format(interaction[O_TELNR_MOBILE]))
                if interaction[O_TELNR_MOBILE] != '':
                    logger.info("if interaction[O_TELNR_MOBILE] != ''")
                    match_phone = re.search(PHONE_REGEX, interaction[O_TELNR_MOBILE])
                    if match_phone:
                        logger.info("if match_phone")
                        generate_empty_attributes(interaction, O_INTERACTION_FIELDS)
                        if contact_id in contacts.keys():
                            logger.info("if contact_id in contacts.keys()")
                            if contact_id in interactions_to_write:
                                logger.info("if contact_id in interactions_to_write")
                                interactions_to_write[contact_id].append(interaction)
                            else:
                                logger.info("if not contact_id in interactions_to_write")
                                interactions_to_write[contact_id] = [interaction]
                        else:
                            raise Exception(MSG_DISCARDED_CONTACT)
                    else:
                        raise Exception(MSG_INVALID_PHONE)
                else:
                    raise Exception(MSG_EMPTY_PHONE)
        except Exception as e:
            # Agrega una interacción por aplicación instalada
            for app in apps_installed:
                discarded = {}
                discarded[O_DISCARD_MOTIVE] = e.args[0]
                if app == I_FLAG_APP_CONS:
                    if O_ID_ORIGIN not in discarded.keys():
                        discarded[O_ID_ORIGIN] = APP_CONS_ID_ORIGIN
                    if O_ID not in discarded.keys():
                        discarded[O_ID] = str(row[I_TOKEN_APP_CONS]).strip()
                elif app == I_FLAG_APP_SOCIA:
                    if O_ID_ORIGIN not in discarded.keys():
                        discarded[O_ID_ORIGIN] = APP_SOCIA_ID_ORIGIN
                    if O_ID not in discarded.keys():
                        discarded[O_ID] = str(row[I_TOKEN_APP_SOCIA]).strip()
                if O_COMM_MEDIUM not in discarded.keys():
                    discarded[O_COMM_MEDIUM] = 'MOBILE_APP'
                if O_IA_TYPE not in discarded.keys():
                    discarded[O_IA_TYPE] = 'MOB_APP_INSTALLED'
                if O_DEVICE_TYPE not in discarded.keys():
                    discarded[O_DEVICE_TYPE] = 'PHONE'
                if O_TIMESTAMP not in discarded.keys():
                    discarded[O_TIMESTAMP] = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S')
                if O_NAME_FIRST not in discarded.keys():
                    discarded[O_NAME_FIRST] = str(row[I_PRIMER_NOMBRE]).strip()
                if O_NAME_LAST not in discarded.keys():
                    discarded[O_NAME_LAST] = str(row[I_APE_PATERNO]).strip()
                if O_TELNR_MOBILE not in discarded.keys():
                    discarded[O_TELNR_MOBILE] = str(row[I_TEL_MOVIL]).strip()
                generate_empty_attributes(discarded, O_INTERACTION_FIELDS)
                interactions_to_discard[contact_id] = discarded
            for key in row.keys():
                row[key] = str(row[key])
            logger.error('Discarded {}: {}'.format(e.args[0], json.dumps(row)))
    logger.info('Lines read: {} - To write: {} - Discarded: {}'.
                format(read_counter, len(interactions_to_write), len(interactions_to_discard)))
    return interactions_to_write, interactions_to_discard


def generate_campanas_consultoras(campanas_consultoras, contacts):
    logger = logging.getLogger('{}.generate_campanas_consultoras'.format(LOGGER_NAME))
    logger.debug('Processing input')
    logger.debug('Required fields: {}'.format(I_FIELDS_CAMPANAS_CONSULTORA))
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
                    raise Exception(MSG_INPUT_ERROR.format(key))
                else:
                    discarded[key] = row[key]

            # CUSTOM VALIDATIONS
            try:
                campana_consultora[O_COD_PAIS] = row[I_COD_PAIS]
                if len(campana_consultora[O_COD_PAIS]) != 2:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_COD_PAIS))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_COD_PAIS))

            try:
                campana_consultora[O_COD_REGION] = format_text(I_COD_REGION, row)
                if len(str(campana_consultora[O_COD_REGION])) > 3:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_COD_REGION))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_COD_REGION))

            try:
                campana_consultora[O_COD_ZONA] = int(row[I_COD_ZONA])
                if len(str(campana_consultora[O_COD_ZONA])) > 4:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_COD_ZONA))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_COD_ZONA))

            try:
                campana_consultora[O_EDAD_BELCORP] = int(row[I_EDAD_BELCORP])
                if len(str(campana_consultora[O_EDAD_BELCORP])) > 4:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_EDAD_BELCORP))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_EDAD_BELCORP))

            try:
                campana_consultora[O_COD_COMPORTAMIENTO] = int(row[I_COD_COMPORTAMIENTO])
                if campana_consultora[O_COD_COMPORTAMIENTO] not in range(0, 8):
                    raise Exception(MSG_INVALID_DOMAIN.format(I_COD_COMPORTAMIENTO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_COD_COMPORTAMIENTO))

            try:
                campana_consultora[O_DESC_SEGMENTO] = row[I_DESC_SEGMENTO]
                if campana_consultora[O_DESC_SEGMENTO] not in [x[1] for x in D_SEGMENTOS]:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_DESC_SEGMENTO))
                else:
                    if [campana_consultora[O_COD_COMPORTAMIENTO], campana_consultora[O_DESC_SEGMENTO]] \
                            not in D_SEGMENTOS:
                        raise Exception(
                            'Attributes "{}"-"{}" invalid tuple'.format(I_COD_COMPORTAMIENTO, I_DESC_SEGMENTO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_DESC_SEGMENTO))

            try:
                campana_consultora[O_TIPO_CONSULTORA] = row[I_TIPO_CONSULTORA]
                if campana_consultora[O_TIPO_CONSULTORA] not in D_TIPO_CONSULTORA:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_TIPO_CONSULTORA))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_TIPO_CONSULTORA))

            try:
                campana_consultora[O_DESC_CONSTANCIA_NUEVAS] = row[I_DESC_CONSTANCIA_NUEVAS]
                if campana_consultora[O_DESC_CONSTANCIA_NUEVAS] != '' and \
                                campana_consultora[O_DESC_CONSTANCIA_NUEVAS] not in D_CONSTANCIA_NUEVAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_DESC_CONSTANCIA_NUEVAS))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_DESC_CONSTANCIA_NUEVAS))

            try:
                campana_consultora[O_MARCA_LANZAMIENTO] = format_text(I_MARCA_LANZAMIENTO, row)
                if campana_consultora[O_MARCA_LANZAMIENTO] != '' and \
                                campana_consultora[O_MARCA_LANZAMIENTO] not in D_MARCAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_MARCA_LANZAMIENTO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_MARCA_LANZAMIENTO))

            try:
                campana_consultora[O_MARCA_TOP] = format_text(I_MARCA_TOP, row)
                if campana_consultora[O_MARCA_TOP] != '' and \
                                campana_consultora[O_MARCA_TOP] not in D_MARCAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_MARCA_TOP))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_MARCA_TOP))

            try:
                campana_consultora[O_CAT_LANZAMIENTO] = format_text(I_CAT_LANZAMIENTO, row)
                if campana_consultora[O_CAT_LANZAMIENTO] != '' and \
                                campana_consultora[O_CAT_LANZAMIENTO] not in D_CATEGORIAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_CAT_LANZAMIENTO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_CAT_LANZAMIENTO))

            try:
                campana_consultora[O_CAT_TOP] = format_text(I_CAT_TOP, row)
                if campana_consultora[O_CAT_TOP] != '' and \
                                campana_consultora[O_CAT_TOP] not in D_CATEGORIAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_CAT_TOP))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_CAT_TOP))

            try:
                campana_consultora[O_COD_VTA_LANZAMIENTO] = format_text(I_COD_VTA_LANZAMIENTO, row)
                if len(campana_consultora[O_COD_VTA_LANZAMIENTO]) not in range(0, 6):
                    raise Exception(MSG_INVALID_DOMAIN.format(I_COD_VTA_LANZAMIENTO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_COD_VTA_LANZAMIENTO))

            try:
                campana_consultora[O_COD_VTA_TOP] = format_text(I_COD_VTA_TOP, row)
                if len(campana_consultora[O_COD_VTA_TOP]) not in range(0, 6):
                    raise Exception(MSG_INVALID_DOMAIN.format(I_COD_VTA_TOP))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_COD_VTA_TOP))

            try:
                campana_consultora[O_DESC_MARCA_SCORE] = format_text(I_DESC_MARCA_SCORE, row)
                if campana_consultora[O_DESC_MARCA_SCORE] == '0':
                    campana_consultora[O_DESC_MARCA_SCORE] = ''
                if campana_consultora[O_DESC_MARCA_SCORE] != '' and \
                                campana_consultora[O_DESC_MARCA_SCORE] not in D_MARCAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_DESC_MARCA_SCORE))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_DESC_MARCA_SCORE))

            try:
                campana_consultora[O_DESC_CAT_SCORE] = format_text(I_DESC_CAT_SCORE, row)
                if campana_consultora[O_DESC_CAT_SCORE] == '0':
                    campana_consultora[O_DESC_CAT_SCORE] = ''
                if campana_consultora[O_DESC_CAT_SCORE] != '' and \
                                campana_consultora[O_DESC_CAT_SCORE] not in D_CATEGORIAS:
                    raise Exception(MSG_INVALID_DOMAIN.format(I_DESC_CAT_SCORE))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_DESC_CAT_SCORE))

            # INTEGERS
            try:
                campana_consultora[O_ANIO_CAMPANA_EXPOSICION] = int(row[I_ANIO_CAMPANA_EXPOSICION][0:4])
                campana_consultora[O_NRO_CAMPANA_EXPOSICION] = int(row[I_ANIO_CAMPANA_EXPOSICION][4:6])
                if campana_consultora[O_NRO_CAMPANA_EXPOSICION] not in range(1, 19):
                    raise Exception(MSG_INVALID_DOMAIN.format(I_ANIO_CAMPANA_EXPOSICION))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_ANIO_CAMPANA_EXPOSICION))
            try:
                campana_consultora[O_ANIO_CAMPANA_INGRESO] = int(row[I_ANIO_CAMPANA_INGRESO][0:4])
                campana_consultora[O_NRO_CAMPANA_INGRESO] = int(row[I_ANIO_CAMPANA_INGRESO][4:6])
                if campana_consultora[O_NRO_CAMPANA_INGRESO] not in range(1, 19):
                    raise Exception(MSG_INVALID_DOMAIN.format(I_ANIO_CAMPANA_INGRESO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(I_ANIO_CAMPANA_INGRESO))
            try:
                campana_consultora[O_ANIO_CAMPANA_PROCESO] = int(row[I_ANIO_CAMPANA_PROCESO][0:4])
                campana_consultora[O_NRO_CAMPANA_PROCESO] = int(row[I_ANIO_CAMPANA_PROCESO][4:6])
                if campana_consultora[O_NRO_CAMPANA_PROCESO] not in range(1, 19):
                    raise Exception(MSG_INVALID_DOMAIN.format(O_NRO_CAMPANA_PROCESO))
            except ValueError:
                raise Exception(MSG_INVALID_TYPE.format(O_NRO_CAMPANA_PROCESO))
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

                # DATES
                campana_consultora[O_FECHA_INICIO_VENTA] = format_date(I_FECHA_INICIO_VENTA, row)
                campana_consultora[O_FECHA_FIN_VENTA] = format_date(I_FECHA_FIN_VENTA, row)
                campana_consultora[O_FECHA_INICIO_FACTURACION] = format_date(I_FECHA_INICIO_FACTURACION, row)
                campana_consultora[O_FECHA_FIN_FACTURACION] = format_date(I_FECHA_FIN_FACTURACION, row)
                campana_consultora[O_FECHA_ENVIO] = format_date(I_FECHA_ENVIO, row)

                # DECIMALS
                campana_consultora[O_SCORE_MARCA] = format_decimal(I_SCORE_MARCA, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_CATEGORIA] = format_decimal(I_SCORE_CATEGORIA, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TOP] = format_decimal(I_SCORE_TOP, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_LANZAMIENTO] = \
                    format_decimal(I_SCORE_LANZAMIENTO, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_VISITAS] = format_decimal(I_SCORE_VISITAS, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TIP_GESTION_DIGITAL] = \
                    format_decimal(I_SCORE_TIP_GESTION_DIGITAL, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TIP_COBRANZA] = \
                    format_decimal(I_SCORE_TIP_COBRANZA, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_MAS_CLIENTES] = \
                    format_decimal(I_SCORE_MAS_CLIENTES, row, minimum=0.0, maximum=1.0)
                campana_consultora[O_SCORE_TIP_PEDIDO_ONLINE] = format_decimal(I_SCORE_TIP_PEDIDO_ONLINE, row)
                campana_consultora[O_PROBABILIDAD_FUGA] = \
                    format_decimal(I_PROBABILIDAD_FUGA, row, minimum=0.0, maximum=100.0)
                campana_consultora[O_VTA_FACTURADA_UC] = format_decimal(I_VTA_FACTURADA_UC, row)
                campana_consultora[O_PRECIO_LANZAMIENTO] = format_decimal(I_PRECIO_LANZAMIENTO, row)
                campana_consultora[O_PRECIO_TOP] = format_decimal(I_PRECIO_TOP, row)
                campana_consultora[O_MONTO_DEUDA] = format_decimal(I_MONTO_DEUDA, row)
                campana_consultora[O_MAX_VTA_FACTURADA_PU5C] = format_decimal(I_MAX_VTA_FACTURADA_PU5C, row)

                # TEXTS
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
                raise Exception(ve.args[0])

            if len(str(int(row[I_COD_EBELISTA]))) > 15:
                raise Exception(MSG_INVALID_DOMAIN.format(I_COD_EBELISTA))
            campana_consultora[O_COD_EBELISTA] = \
                str(int(row[I_COD_EBELISTA])) + '_' + str(campana_consultora[O_COD_PAIS])
            campana_consultora[O_ID_CAMPANA_CONSULTORA] = str(campana_consultora[O_ANIO_CAMPANA_EXPOSICION]) + \
                                                          str(campana_consultora[O_NRO_CAMPANA_EXPOSICION]).zfill(2) + \
                                                          '_' + str(campana_consultora[O_COD_EBELISTA])
            campana_consultora[O_IDORIGIN] = 'SAP_ODATA_IMPORT'
            if campana_consultora[O_COD_EBELISTA] in contacts.keys():
                campanas_consultoras_to_write[campana_consultora[O_ID_CAMPANA_CONSULTORA]] = campana_consultora
            else:
                raise Exception(MSG_DISCARDED_CONTACT)
        except Exception as e:
            discarded = campana_consultora.copy()
            discarded[O_DISCARD_MOTIVE] = e.args[0]
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
                discarded[O_COD_EBELISTA] = str(row[I_COD_EBELISTA]).strip() + '_' + \
                                            str(row[I_COD_PAIS]).strip()
            if O_ID_CAMPANA_CONSULTORA not in discarded.keys():
                discarded[O_ID_CAMPANA_CONSULTORA] = str(row[I_ANIO_CAMPANA_EXPOSICION][0:4]).strip() + \
                                                     str(row[I_ANIO_CAMPANA_EXPOSICION][4:6]).strip().zfill(2) + '_' + \
                                                     str(row[I_COD_EBELISTA]).strip() + '_' + \
                                                     str(row[I_COD_PAIS]).strip()
            if O_IDORIGIN not in discarded.keys():
                discarded[O_IDORIGIN] = 'SAP_ODATA_IMPORT'
            generate_empty_attributes(discarded, O_CAMPANA_CONSULTORA_FIELDS)
            campanas_consultoras_to_discard[discarded[O_ID_CAMPANA_CONSULTORA]] = discarded
            for key in row.keys():
                row[key] = str(row[key])
            logger.error('Discarded {}: {}'.format(discarded[O_DISCARD_MOTIVE], json.dumps(row)))
    logger.info('Lines read: {} - To write: {} - Discarded: {}'.
                format(read_counter, len(campanas_consultoras_to_write), len(campanas_consultoras_to_discard)))
    return campanas_consultoras_to_write, campanas_consultoras_to_discard


def from_csv(input):
    logger = logging.getLogger('{}.from_csv'.format(LOGGER_NAME))
    logger.info('Starting')
    source_folder, source_file = os.path.split(os.path.abspath(input))
    input_file = os.path.join(source_folder, source_file)
    logger.info(source_folder)
    logger.info(source_file)
    logger.info(input_file)
    with open(input_file, 'r', encoding=SOURCE_ENCODING) as ifile:
        reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
        contacts_to_write, contacts_to_discard = generate_contacts(reader)
        # Resetea la lectura del archivo para tomar las interacciones
        ifile.seek(0)
        reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
        interactions_to_write, interactions_to_discard = generate_interactions(reader, contacts_to_write)
        # Resetea la lectura del archivo para tomar las campanas_consultoras
        ifile.seek(0)
        reader = csv.DictReader(ifile, delimiter=SOURCE_DELIMITER)
        campanas_consultoras_to_write, campanas_consultoras_to_discard = generate_campanas_consultoras(reader,
                                                                                                       contacts_to_write)
    return contacts_to_write, interactions_to_write, campanas_consultoras_to_write


def from_sql(server, database, user, password):
    logger = logging.getLogger('{}.from_sql'.format(LOGGER_NAME))
    logger.info('Starting')
    sql_access = SqlServerAccess(server, database, user, password)
    conn = sql_access.connect()
    # WIN: prefix DB to the query otherwise Invalid Object error
    query = VIRTUAL_COACH_CONSULTORAS_QUERY.format(database)
    logger.debug('Executing query: {}'.format(query))
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    query_result = []
    for row in cursor.fetchall():
        query_result.append(dict(zip(columns, row)))
    logger.info('Rows retrieved: {}'.format(len(query_result)))
    contacts_to_write, contacts_to_discard = generate_contacts(query_result)
    interactions_to_write, interactions_to_discard = generate_interactions(query_result, contacts_to_write)
    campanas_consultoras_to_write, campanas_consultoras_to_discard = generate_campanas_consultoras(query_result,
                                                                                                   contacts_to_write)
    return contacts_to_write, interactions_to_write, campanas_consultoras_to_write


def to_odata(contacts, interactions, campanas_consultoras, contact_type):
    logger = logging.getLogger('{}.to_odata'.format(LOGGER_NAME))
    logger.info('Starting')
    business_objects = {
        ODATA_CONTACT: contacts,
        ODATA_INTERACTION: interactions,
        ODATA_CAMPANA_CONSULTORA: campanas_consultoras
    }
    odata_access = ODataAccess(contact_type)
    odata_access.post_data(business_objects)


def to_csv(output, contacts, interactions, campanas_consultoras):
    logger = logging.getLogger('{}.to_csv'.format(LOGGER_NAME))
    logger.info('Starting')
    output_folder, output_file = os.path.split(os.path.abspath(output))
    # CONTACTS
    file = os.path.join(output_folder, PREFIX_CONTACT + '_' + output_file)
    write_output_file(file, contacts, output_file_type=PREFIX_CONTACT, discard=False)
    # CAMPANAS_CONSULTORAS
    file = os.path.join(output_folder, PREFIX_CAMPANA_CONSULTORA + '_' + output_file)
    write_output_file(file, campanas_consultoras, output_file_type=PREFIX_CAMPANA_CONSULTORA, discard=False)
    # INTERACTIONS
    file = os.path.join(output_folder, PREFIX_INTERACTION + '_' + output_file)
    write_output_file(file, interactions, output_file_type=PREFIX_INTERACTION, discard=False)


def init_logging():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s[%(name)s] - %(message)s')
    # INFO Handler
    fh = logging.handlers.TimedRotatingFileHandler(LOGGING_FILE + '_INFO', when='midnight')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # DEBUG Handler
    dh = logging.handlers.TimedRotatingFileHandler(LOGGING_FILE + '_DEBUG', when='midnight')
    dh.setLevel(logging.DEBUG)
    dh.setFormatter(formatter)
    logger.addHandler(dh)
    # ERROR Handler
    eh = logging.handlers.TimedRotatingFileHandler(LOGGING_FILE + '_ERROR', when='midnight')
    eh.setLevel(logging.ERROR)
    eh.setFormatter(formatter)
    logger.addHandler(eh)
    # STREAM Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


if __name__ == '__main__':
    init_logging()
    try:
        parser = argparse.ArgumentParser(description='Belcorp ETL to Hybris Marketing', add_help=False)
        group = parser.add_mutually_exclusive_group(required=True)
        # Add arguments
        group.add_argument('--sql2odata', action='store_true')
        group.add_argument('--sql2csv', action='store_true')
        group.add_argument('--csv2csv', action='store_true')
        group.add_argument('--csv2odata', action='store_true')

        # SQL2ODATA
        parser_sql2odata = argparse.ArgumentParser(description='sql2odata', add_help=False)
        parser_sql2odata.add_argument('--sql2odata', action='store_true', required=True)
        parser_sql2odata.add_argument('-s', '--server', type=str, required=True)
        parser_sql2odata.add_argument('-d', '--database', type=str, required=True)
        parser_sql2odata.add_argument('-u', '--user', type=str, required=True)
        parser_sql2odata.add_argument('-p', '--password', type=str, required=True)
        parser_sql2odata.add_argument('-c', '--contact_type', type=str, choices=['B2B', 'B2C'], required=True)

        # SQL2CSV
        parser_sql2csv = argparse.ArgumentParser(description='sql2csv', add_help=False)
        parser_sql2csv.add_argument('--sql2csv', action='store_true', required=True)
        parser_sql2csv.add_argument('-s', '--server', type=str, required=True)
        parser_sql2csv.add_argument('-d', '--database', type=str, required=True)
        parser_sql2csv.add_argument('-u', '--user', type=str, required=True)
        parser_sql2csv.add_argument('-p', '--password', type=str, required=True)
        parser_sql2csv.add_argument('-o', '--output', type=str, required=True)

        # CSV2CSV
        parser_csv2csv = argparse.ArgumentParser(description='csv2csv', add_help=False)
        parser_csv2csv.add_argument('--csv2csv', action='store_true', required=True)
        parser_csv2csv.add_argument('-i', '--input', type=str, required=True)
        parser_csv2csv.add_argument('-o', '--output', type=str, required=True)

        # CSV2ODATA
        parser_csv2odata = argparse.ArgumentParser(description='csv2odata', add_help=False)
        parser_csv2odata.add_argument('--csv2odata', action='store_true', required=True)
        parser_csv2odata.add_argument('-i', '--input', type=str, required=True)
        parser_csv2odata.add_argument('-c', '--contact_type', type=str, choices=['B2B', 'B2C'], required=True)

        args, unkwn_args = parser.parse_known_args()
        if args.csv2csv:
            args = parser_csv2csv.parse_args()
            contacts, interactions, campanas_consultoras = from_csv(input=args.input)
            to_csv(output=args.output, contacts=contacts, interactions=interactions, campanas_consultoras=campanas_consultoras)
        elif args.sql2csv:
                args = parser_sql2csv.parse_args()
                contacts, interactions, campanas_consultoras = from_sql(server=args.server,
                                                                        database=args.database,
                                                                        user=args.user,
                                                                        password=args.password)
                to_csv(output=args.output, contacts=contacts, interactions=interactions,
                       campanas_consultoras=campanas_consultoras)
        elif args.csv2odata:
            args = parser_csv2odata.parse_args()
            contacts, interactions, campanas_consultoras = from_csv(input=args.input)
            to_odata(contacts=contacts,
                     interactions=interactions,
                     campanas_consultoras=campanas_consultoras,
                     contact_type=args.contact_type)
        elif args.sql2odata:
            args = parser_sql2odata.parse_args()
            contacts, interactions, campanas_consultoras = from_sql(server=args.server,
                                                                    database=args.database,
                                                                    user=args.user,
                                                                    password=args.password)
            to_odata(contacts=contacts,
                     interactions=interactions,
                     campanas_consultoras=campanas_consultoras,
                     contact_type=args.contact_type)
        else:
            parser_csv2csv.print_usage()
            parser_sql2csv.print_usage()
            parser_csv2odata.print_usage()
            parser_sql2odata.print_usage()
    except Exception as e:
        logger = logging.getLogger(LOGGER_NAME)
        logger.error(e)
        raise(e)
