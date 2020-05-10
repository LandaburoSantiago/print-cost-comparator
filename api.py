import os
from flask import Flask
from flask import render_template, request
from datetime import datetime, date, timedelta
import funciones_bbdd

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def inicio():
    return render_template('principal.html')


@app.route('/librerias_gchu', methods=['GET', 'POST'])
def librerias_gchu():
    if request.method == "POST":
        hora = request.form['idHora']
        minutos = request.form['idMinutos']
        segundos = request.form['idSegundos']
        dia = request.form['idDia']
        ciudad = request.form['city']
        str(hora)
        str(minutos)
        str(segundos)
        int(dia)
        hora_formateada = funciones_bbdd.obtenerHoraFormateada(hora, minutos, segundos)
        hora = datetime.strptime(hora_formateada, "%X").time()
        momento_dia = funciones_bbdd.obtenerMomentoDia(hora)
        listado = funciones_bbdd.listar('gualeguaychu', momento_dia, hora, dia)
        return render_template('librerias_gchu.html', listado=listado, ciudad=ciudad)


@app.route('/librerias_cdelu')
def librerias_cdelu():
    return render_template('librerias_cdelu.html')


@app.route('/mas_detalles', methods=['GET', 'POST'])
def mas_detalles():
    if request.method == "GET":
        id = request.args.get('idFotocopiadora')
        ciudad = request.args.get('idCiudad')
        info = funciones_bbdd.get_one(id, ciudad)
    return render_template('mas_detalles.html', info=info)


@app.route('/error_sin_red')
def error_sin_red():
    return render_template('error_sin_red.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)
