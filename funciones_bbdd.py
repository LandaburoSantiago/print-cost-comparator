from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, date, timedelta


# VARIABLES GLOBALES HORA Y DIA DEL SISTEMA
def obtenerHoraFormateada(hora, minutos, segundos):
    hora_formateada = ''
    if len(hora) == 1:
        hora = '0'+hora
    if len(minutos) == 1:
        minutos = '0' + minutos
    if len(segundos) == 1:
        segundos = '0' + segundos
    hora_formateada = hora + ':' + minutos + ':' + segundos
    return hora_formateada


def obtenerMomentoDia(hora):
    # SI LA HORA DEL SISTEMA ESTA ENTRE LAS 6:00 Y LAS 13:30 SE DEDUCE QUE ES DE MANIANA
    if hora >= datetime.strptime("06:00:00", "%X").time() and hora < datetime.strptime("13:30:00", "%X").time():
        momento_dia = 'maniana'
    # SI LA HORA DEL SISTEMA ESTA ENTRE LAS 13:30 Y LAS 21:00 SE DEDUCE QUE ES DE TADE
    elif hora >= datetime.strptime("13:30:00", "%X").time() and hora < datetime.strptime("21:00:00", "%X").time():
        momento_dia = 'tarde'
    # SI LA HORA DEL SISTEMA ES MAYOR QUE LAS 21 SE DEDUCE QUE ES DE NOCHE
    else:
        momento_dia = 'noche'
    return momento_dia


def conexion():
    client = MongoClient("mongodb+srv://Santi:proyectofotocopiadoras@cluster0-gs6ij.mongodb.net/test?retryWrites=true&w=majority")
    db = client.fotocopiadoras
    return db


'''
def guardar(documento):
    db = conexion()
    db.get_collection('fotocopiadoras').insert(documento)
'''


# recibe como parametro cantidad_paginas y ciudad hace una consulta a la base de datos
# y devuelve los datos procesados en una lista ordenada por el precio total
def listar_color(cantidad_paginas, simple_doble, ciudad, momento_dia, hora, dia):
    db = conexion()
    documento = db.get_collection('fotocopiadoras_'+ciudad).find()
    lista = []
    if simple_doble == 'doblefaz':
        # AL SER DOBLE FAZ SE DIVIDE LA CANTIDAD DE PAGINAS POR 2
        if (cantidad_paginas % 2 == 0):
            cantidad_paginas = cantidad_paginas // 2
        else:
            cantidad_paginas = cantidad_paginas // 2
            cantidad_paginas += 1
    for i in documento:
        # CONVERTIR EL PRECIO DE LA FOTOCOPIA A FLOAT REALIZA EL CALCULO
        precio = float(i['precio_fotocopia_color'])*cantidad_paginas
        # FORMATEA EL NUMERO PARA QUE TENGA LA FORMA N.NN
        precio = "{0: .2f}".format(precio)
        # SI EL DIA ES 7(DOMINGO) LA SITUACION SE PONE EN 'CERRADO' AUTOMATICAMENTE
        if dia != 0:
            # SI NO ES DOMINGO SE PREGUNTA SI ES SABADO
            if dia == 6:
                # SI ES SABADO SE PREGUNTA SI EL SABADO DE TARDE ABRE
                if i['sabado_tarde'] == 'si':
                    # SI SABADO DE TARDE ABRE PREGUNTA SI ES DE MANIANA
                    if momento_dia == 'maniana':
                        # TOMA LOS VALORES DE HORARIO APRETURA Y CIERRE DE MANIANA
                        hora_a = i['hora_apertura_maniana']
                        hora_c = i['hora_cierre_maniana']
                        # PREGUNTA SI LA HORA DEL SISTEMA ESTA DENTRO DEL RANGO DE HORARIO DE APERTURA Y CIERRE DE MANIANA
                        if hora >= datetime.strptime(i['hora_apertura_maniana']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_maniana']+":00", "%X").time():
                            # SI ESTA DENTRO DEL RANGO LA SITUACION ES ABIERTO
                            situacion = 'abierto'
                        else:
                            # SI NO ESTA DENTRO DEL RANGO LA SITUACION ES CERRADO
                            situacion = 'cerrado'
                    # SI EL MOMENTO DEL DIA NO ES MANIANA PREGUNTA SI ES DE TARDE
                    elif momento_dia == 'tarde':
                        # TOMA LOS VALORES DE HORARIO APRETURA Y CIERRE DE TARDE
                        hora_a = i['hora_apertura_tarde']
                        hora_c = i['hora_cierre_tarde']
                        # PREGUNTA SI LA HORA DEL SISTEMA ESTA DENTRO DEL RANGO DE HORARIO DE APERTURA Y CIERRE DE TARDE
                        if hora >= datetime.strptime(i['hora_apertura_tarde']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_tarde']+":00", "%X").time():
                            # SI ESTA DENTRO DEL RANGO LA SITUACION ES ABIERTO
                            situacion = 'abierto'
                        else:
                            # SI NO ESTA DENTRO DEL RANGO LA SITUACION ES CERRADO
                            situacion = 'cerrado'
                    # SI EL MOMENTO DEL DIA NO ES TARDE PREGUNTA SI ES DE NOCHE
                    elif momento_dia == 'noche':
                        # TOMA LOS VALORES DE APERTURA Y CIERRE DE MANIANA
                        hora_a = i['hora_apertura_maniana']
                        hora_c = i['hora_cierre_maniana']
                        # Y LA SITUACION ES CERRADO
                        situacion = 'cerrado'
                    # SI EL SABADO DE TARDE NO ABRE
                    else:
                        # HACE LAS MISMAS PREGUNTAS PERO SOLAMENTE PARA EL MOMENTO DEL DIA DE MANIANA
                        if momento_dia == 'maniana':
                            hora_a = i['hora_apertura_maniana']
                            hora_c = i['hora_cierre_maniana']
                            if hora >= datetime.strptime(i['hora_apertura_maniana']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_maniana']+":00", "%X").time():
                                situacion = 'abierto'
                            else:
                                situacion = 'cerrado'
                        else:
                            # SI NO ES DE MANIANA SE COLOCA LA SITUACION EN CERRADO Y LOS HORARIOS DE MANIANA
                            hora_a = i['hora_apertura_maniana']
                            hora_c = i['hora_cierre_maniana']
                            situacion = 'cerrado'
            # SI EL DIA NO ES SABADO
            else:
                # SE HACEN LAS MISMAS PREGUNTAS PARA TODOS LOS MOMENTOS DEL DIA
                if momento_dia == 'maniana':
                    hora_a = i['hora_apertura_maniana']
                    hora_c = i['hora_cierre_maniana']
                    if hora >= datetime.strptime(i['hora_apertura_maniana']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_maniana']+":00", "%X").time():
                        situacion = 'abierto'
                    else:
                        situacion = 'cerrado'
                elif momento_dia == 'tarde':
                    hora_a = i['hora_apertura_tarde']
                    hora_c = i['hora_cierre_tarde']
                    if hora >= datetime.strptime(i['hora_apertura_tarde']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_tarde']+":00", "%X").time():
                        situacion = 'abierto'
                    else:
                        situacion = 'cerrado'
                elif momento_dia == 'noche':
                    hora_a = i['hora_apertura_maniana']
                    hora_c = i['hora_cierre_maniana']
                    situacion = 'cerrado'
        # SI EL DIA ES 7(DOMINGO) SE PONE LA SITUACION EN CERRADO Y LOS HORARIOS DE MANIANA
        else:
            hora_a = i['hora_apertura_maniana']
            hora_c = i['hora_cierre_maniana']
            situacion = 'cerrado'
        # SE ARMA UN DICCIONARIO CON TODOS LOS CAMPOS
        diccionario = {
            'id': i['_id'],
            'nombre': i['nombre'],
            'precio_total': precio,
            'precio_fotocopia_color': i['precio_fotocopia_color'],
            'precio_fotocopia_byn': i['precio_fotocopia_byn'],
            'mail': i['mail'],
            'telefono': i['telefono'],
            'direccion': i['direccion'],
            # SE AGREGA HORA_APERTURA Y HORA_CIERRE PARA MOSTRAR EN EL HTML
            'hora_apertura': hora_a,
            'hora_cierre': hora_c,
            # LA SITUACION ES PARA INDICARLO EN EL HTML SI ES ABIERTO O CERRADO
            'abierto_cerrado': situacion
        }
        # LOS DICCIONARIOS ARMADOS SE GUARDAN EN UNA LISTA
        lista.append(diccionario)
    # LA LISTA SE ORDENA POR EL CAMPO PRECIO_TOTAL
    lista.sort(key=lambda k: k['precio_total'])
    return lista


# recibe como parametro cantidad_paginas y ciudad hace una consulta a la base de datos
# y devuelve los datos procesados en una lista ordenada por el precio total
def listar_byn(cantidad_paginas, simple_doble, ciudad, momento_dia, hora, dia):
    db = conexion()
    documento = db.get_collection('fotocopiadoras_'+ciudad).find()
    lista = []
    # AL SER DOBLE FAZ SE DIVIDE LA CANTIDAD DE PAGINAS POR 2
    if simple_doble == 'doblefaz':
        if (cantidad_paginas % 2 == 0):
            cantidad_paginas = cantidad_paginas // 2
        else:
            cantidad_paginas = cantidad_paginas // 2
            cantidad_paginas += 1
            print(cantidad_paginas)
    for i in documento:
        # CONVERTIR EL PRECIO DE LA FOTOCOPIA A FLOAT REALIZA EL CALCULO
        precio = float(i['precio_fotocopia_byn'])*cantidad_paginas
        # FORMATEA EL NUMERO PARA QUE TENGA LA FORMA N.NN
        precio = "{0: .2f}".format(precio)
        # SI EL DIA ES 7(DOMINGO) LA SITUACION SE PONE EN 'CERRADO' AUTOMATICAMENTE
        if dia != 7:
            # SI NO ES DOMINGO SE PREGUNTA SI ES SABADO
            if dia == 6:
                # SI ES SABADO SE PREGUNTA SI EL SABADO DE TARDE ABRE
                if i['sabado_tarde'] == 'si':
                    # SI SABADO DE TARDE ABRE PREGUNTA SI ES DE MANIANA
                    if momento_dia == 'maniana':
                        # TOMA LOS VALORES DE HORARIO APRETURA Y CIERRE DE MANIANA
                        hora_a = i['hora_apertura_maniana']
                        hora_c = i['hora_cierre_maniana']
                        # PREGUNTA SI LA HORA DEL SISTEMA ESTA DENTRO DEL RANGO DE HORARIO DE APERTURA Y CIERRE DE MANIANA
                        if hora >= datetime.strptime(i['hora_apertura_maniana']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_maniana']+":00", "%X").time():
                            # SI ESTA DENTRO DEL RANGO LA SITUACION ES ABIERTO
                            situacion = 'abierto'
                        else:
                            # SI NO ESTA DENTRO DEL RANGO LA SITUACION ES CERRADO
                            situacion = 'cerrado'
                    # SI EL MOMENTO DEL DIA NO ES MANIANA PREGUNTA SI ES DE TARDE
                    elif momento_dia == 'tarde':
                        # TOMA LOS VALORES DE HORARIO APRETURA Y CIERRE DE TARDE
                        hora_a = i['hora_apertura_tarde']
                        hora_c = i['hora_cierre_tarde']
                        # PREGUNTA SI LA HORA DEL SISTEMA ESTA DENTRO DEL RANGO DE HORARIO DE APERTURA Y CIERRE DE TARDE
                        if hora >= datetime.strptime(i['hora_apertura_tarde']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_tarde']+":00", "%X").time():
                            # SI ESTA DENTRO DEL RANGO LA SITUACION ES ABIERTO
                            situacion = 'abierto'
                        else:
                            # SI NO ESTA DENTRO DEL RANGO LA SITUACION ES CERRADO
                            situacion = 'cerrado'
                    # SI EL MOMENTO DEL DIA NO ES TARDE PREGUNTA SI ES DE NOCHE
                    elif momento_dia == 'noche':
                        # TOMA LOS VALORES DE APERTURA Y CIERRE DE MANIANA
                        hora_a = i['hora_apertura_maniana']
                        hora_c = i['hora_cierre_maniana']
                        # Y LA SITUACION ES CERRADO
                        situacion = 'cerrado'
                    # SI EL SABADO DE TARDE NO ABRE
                    else:
                        # HACE LAS MISMAS PREGUNTAS PERO SOLAMENTE PARA EL MOMENTO DEL DIA DE MANIANA
                        if momento_dia == 'maniana':
                            hora_a = i['hora_apertura_maniana']
                            hora_c = i['hora_cierre_maniana']
                            if hora >= datetime.strptime(i['hora_apertura_maniana']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_maniana']+":00", "%X").time():
                                situacion = 'abierto'
                            else:
                                situacion = 'cerrado'
                        # SI NO ES DE MANIANA SE COLOCA LA SITUACION EN CERRADO Y LOS HORARIOS DE MANIANA
                        else:
                            hora_a = i['hora_apertura_maniana']
                            hora_c = i['hora_cierre_maniana']
                            situacion = 'cerrado'
            # SI EL DIA NO ES SABADO
            else:
                # SE HACEN LAS MISMAS PREGUNTAS PARA TODOS LOS MOMENTOS DEL DIA
                if momento_dia == 'maniana':
                    hora_a = i['hora_apertura_maniana']
                    hora_c = i['hora_cierre_maniana']
                    if hora >= datetime.strptime(i['hora_apertura_maniana']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_maniana']+":00", "%X").time():
                        situacion = 'abierto'
                    else:
                        situacion = 'cerrado'
                elif momento_dia == 'tarde':
                    hora_a = i['hora_apertura_tarde']
                    hora_c = i['hora_cierre_tarde']
                    if hora >= datetime.strptime(i['hora_apertura_tarde']+":00", "%X").time() and hora < datetime.strptime(i['hora_cierre_tarde']+":00", "%X").time():
                        situacion = 'abierto'
                    else:
                        situacion = 'cerrado'
                elif momento_dia == 'noche':
                    hora_a = i['hora_apertura_maniana']
                    hora_c = i['hora_cierre_maniana']
                    situacion = 'cerrado'
        # SI EL DIA ES 7(DOMINGO) SE PONE LA SITUACION EN CERRADO Y LOS HORARIOS DE MANIANA
        else:
            hora_a = i['hora_apertura_maniana']
            hora_c = i['hora_cierre_maniana']
            situacion = 'cerrado'
        # SE ARMA UN DICCIONARIO CON TODOS LOS CAMPOS
        diccionario = {
            'id': i['_id'],
            'nombre': i['nombre'],
            'precio_total': precio,
            'precio_fotocopia_color': i['precio_fotocopia_color'],
            'precio_fotocopia_byn': i['precio_fotocopia_byn'],
            'mail': i['mail'],
            'telefono': i['telefono'],
            'direccion': i['direccion'],
            # SE AGREGA HORA_APERTURA Y HORA_CIERRE PARA MOSTRAR EN EL HTML
            'hora_apertura': hora_a,
            'hora_cierre': hora_c,
            # LA SITUACION ES PARA INDICARLO EN EL HTML SI ES ABIERTO O CERRADO
            'abierto_cerrado': situacion
        }
        # LOS DICCIONARIOS ARMADOS SE GUARDAN EN UNA LISTA
        lista.append(diccionario)
    # LA LISTA SE ORDENA POR EL CAMPO PRECIO_TOTAL
    lista.sort(key=lambda k: k['precio_total'])
    return lista


def get_one(id, ciudad):
    db = conexion()
    documento = db.get_collection('fotocopiadoras_'+ciudad).find_one({"_id": ObjectId(id)})
    documento['_id'] = str(documento['_id'])
    return documento
