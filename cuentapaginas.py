import PyPDF2


def contar_paginas(directorio, nombre_archivo):
    ruta_archivo = directorio+'/'+nombre_archivo
    archivo = open(ruta_archivo)
    leer_pdf = PyPDF2.PdfFileReader(archivo)
    numero_de_paginas = leer_pdf.getNumPages()
    return numero_de_paginas
