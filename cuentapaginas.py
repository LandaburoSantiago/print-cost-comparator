import re
import os

rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE | re.DOTALL)


def count_pages(filename):
    data = file(filename, "r+b").read()
    return len(rxcountpages.findall(data))


if __name__ == "__main__":
    filename = '/media/santiago/DATOS_LINUX/Pagina fotocopias/Mas de polimorfismo y herencia.pdf'
    print count_pages(filename)
