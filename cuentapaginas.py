import PyPDF2


def contar_paginas(directorio, nombre_archivo):
    ruta_archivo = directorio+'/'+nombre_archivo
    leer_pdf = PyPDF2.PdfFileReader(open(ruta_archivo, mode='rb'))
    numero_de_paginas = leer_pdf.getNumPages()
    return numero_de_paginas
