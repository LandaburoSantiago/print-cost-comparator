from firebase import firebase

print('---------CARGAR DATOS DE FOTOCOPIADORAS---------')
control = input("Si es una fotocopiadora de gchu presione 'g' si es de concepcion presione 'c': ")
listo = False
while (control == 'g' or control == 'c') and listo is False:
    diccionario = {
        'nombre': '',
        'precio_fotocopia_color': '',
        'precio_fotocopia_byn': '',
        'mail': '',
        'telefono': '',
        'direccion': '',
        'sabado_tarde': '',
        'hora_apertura_maniana': '',
        'hora_cierre_maniana': '',
        'hora_apertura_tarde': '',
        'hora_cierre_tarde': '',
        'estado': ''
    }
    if control == 'g':
        diccionario['nombre'] = input("Ingrese el nombre de la fotocopiadora: ")
        diccionario['precio_fotocopia_color'] = float(input("Ingrese el precio de la fotocopia a color: "))
        diccionario['precio_fotocopia_byn'] = float(input("Ingrese el precio de la fotocopia en blanco y negro: "))
        diccionario['mail'] = input("Ingrese el mail: ")
        diccionario['telefono'] = input("Ingrese el telefono: ")
        diccionario['direccion'] = input("Ingrese la direccion: ")
        diccionario['sabado_tarde'] = input("Ingrese si o no si abre el sabado de tarde: ")
        diccionario['hora_apertura_maniana'] = input("Ingrese la hora de apertura de maniana: ")
        diccionario['hora_cierre_maniana'] = input("Ingrese la hora de cierre de la maniana: ")
        diccionario['hora_apertura_tarde'] = input("Ingrese la hora de apertura de tarde: ")
        diccionario['hora_cierre_tarde'] = input("Ingrese la hora de cierre de tarde:")
        diccionario['estado'] = True
        id = firebase.post('https://proyecto-fotocopiadoras-bae45.firebaseio.com/fotocopiadoras/fotocopiadoras_cdelu', diccionario)
    elif control == 'c':
        diccionario['nombre'] = input("Ingrese el nombre de la fotocopiadora: ")
        diccionario['precio_fotocopia_color'] = float(input("Ingrese el precio de la fotocopia a color: "))
        diccionario['precio_fotocopia_byn'] = float(input("Ingrese el precio de la fotocopia en blanco y negro: "))
        diccionario['mail'] = input("Ingrese el mail: ")
        diccionario['telefono'] = input("Ingrese el telefono: ")
        diccionario['direccion'] = input("Ingrese la direccion: ")
        diccionario['sabado_tarde'] = input("Ingrese si o no si abre el sabado de tarde: ")
        diccionario['hora_apertura_maniana'] = input("Ingrese la hora de apertura de maniana: ")
        diccionario['hora_cierre_maniana'] = input("Ingrese la hora de cierre de la maniana: ")
        diccionario['hora_apertura_tarde'] = input("Ingrese la hora de apertura de tarde: ")
        diccionario['hora_cierre_tarde'] = input("Ingrese la hora de cierre de tarde:")
        diccionario['estado'] = True
        id = firebase.post('https://proyecto-fotocopiadoras-bae45.firebaseio.com/fotocopiadoras/fotocopiadoras_cdelu', diccionario)
    else:
        print('Error letra desconocida')
    cargar_mas = input("Desea seguir cargando? presione s para SI o n para NO")
    if cargar_mas == 's':
        listo = False
    elif cargar_mas == 'n':
        listo = True
    else:
        print('Error letra desconocida')
