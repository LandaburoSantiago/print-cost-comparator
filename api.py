import os
from flask import Flask
from flask import render_template, request
from cuentapaginas import count_pages
from datetime import datetime, date, timedelta
import funciones_bbdd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/media/santiago/DATOS_LINUX/Archivos_PDF'
directorio = os.path.dirname(__file__)


@app.route('/')
@app.route('/home')
def inicio():
    return render_template('principal.html')


@app.route('/formulario_cdelu_automatico')
def formulario_cdelu_automatico():
    return render_template('formulario_cdelu_automatico.html')


@app.route('/formulario_cdelu_manual')
def formulario_cdelu_manual():
    return render_template('formulario_cdelu_manual.html')


@app.route('/formulario_gchu_automatico')
def formulario_gchu_automatico():
    return render_template('formulario_gchu_automatico.html')


@app.route('/formulario_gchu_manual')
def formulario_gchu_manual():
    return render_template('formulario_gchu_manual.html')


@app.route('/resultados', methods=['GET', 'POST'])
def resultados():
    if request.method == "POST":
        # INICIALIZACION DE LA VARIABLE  CIUDAD
        ciudad = ''
        hora = request.form['idHora']
        minutos = request.form['idMinutos']
        segundos = request.form['idSegundos']
        dia = request.form['idDia']
        str(hora)
        str(minutos)
        str(segundos)
        str(dia)
        hora_formateada = funciones_bbdd.obtenerHoraFormateada(hora, minutos, segundos)
        hora = datetime.strptime(hora_formateada, "%X").time()
        momento_dia = funciones_bbdd.obtenerMomentoDia(hora)
        # SE PREGUNTA SI EL ID CITY QUE VIENE DEL HTML ES GUALEGUAYCHU
        if request.form['city'] == 'gualeguaychu':
            # SE PREGUNTA SI ID DEL MODO QUE VIENE DEL HTML ES AUTOMATICO
            if request.form['modo'] == 'automatico':
                # SI ES AUTOMATICO SE TOMA EL ARCHIVO DEL INPUT TIPO FILE
                f = request.files['entrada_archivos_gchu']
                # LA VARIABLE CIUDAD SE LE ASIGNA GUALEGUAYCHU
                ciudad = 'gualeguaychu'
                # SE GUARDA EL NOMBRE DLE ARCHIVO
                nombre_archivo = f.filename
                # SE GUARDA EL ARCHIVO CON SU NOMBRE EN EL DIRECTORIO
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))
                directorio_actual = os.getcwd()
                os.chdir(os.path.join(app.config['UPLOAD_FOLDER']))
                # SE OBTIENE LA CANTIDAD DE PAGINAS
                cantidad_paginas = count_pages(nombre_archivo)
                os.remove(nombre_archivo)
                os.chdir(directorio_actual)
            # SI EL MODO NO ES AUTOMATICO
            else:
                # SE LE ASIGNA GUALEGUAYCHU A LA VARIABLE CIUDAD
                ciudad = 'gualeguaychu'
                # LA CANTIDAD DE PAGINAS SE OBTIENE DEL INPUT TIPO NUMBER
                cantidad_paginas = request.form['numero']
        # SE REALIZA EL MISMO PROCESO PERO CON LA CIUDAD CDELU
        elif request.form['city'] == 'cdelu':
            if request.form['modo'] == 'automatico':
                f = request.files['entrada_archivos_cdelu']
                ciudad = 'cdelu'
                nombre_archivo = f.filename
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo))
                directorio_actual = os.getcwd()
                os.chdir(os.path.join(app.config['UPLOAD_FOLDER']))
                cantidad_paginas = count_pages(nombre_archivo)
                os.remove(nombre_archivo)
                os.chdir(directorio_actual)
            else:
                ciudad = 'cdelu'
                cantidad_paginas = request.form['numero']
        # OBTENEMOS SI LA FOTOCOPIA ES A COLOR O BLANCO Y NEGRO
        opcion_color_byn = request.form['radio1']
        # Y SI ES SIMPLE O DOBLEahours
        opcion_simple_doble = request.form['radio2']
        # SE CONVIERTE LA CANTIDAD DE PAGINAS A INTEGER
        cantidad_paginas = int(cantidad_paginas)
        # SI ES BLANCO Y NEGRO
        if opcion_color_byn == 'byn':
            # SE LLAMA A LA FUNCION LISTAR_BYN (BLANCO Y NEGRO)
            listado = funciones_bbdd.listar_byn(cantidad_paginas, opcion_simple_doble, ciudad, momento_dia, hora, dia)
        else:
            # SINO SE LLAMA A LA FUNCION LISTAR_COLOR
            listado = funciones_bbdd.listar_color(cantidad_paginas, opcion_simple_doble, ciudad, momento_dia, hora, dia)
        return render_template('resultados.html', listado=listado, ciudad=ciudad)


@app.route('/mas_detalles', methods=['GET', 'POST'])
def mas_detalles():
    if request.method == "GET":
        id = request.args.get('idFotocopiadora')
        print(id)
        ciudad = request.args.get('idCiudad')
        info = funciones_bbdd.get_one(id, ciudad)
    return render_template('mas_detalles.html', info=info)


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=port)
