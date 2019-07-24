import re
import os

rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE | re.DOTALL)


def count_pages(filename):
    data = file(filename, "r+b").read()
    return len(rxcountpages.findall(data))
