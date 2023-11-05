import json
import logging
import re

def findNuvoIp(line):
    '''Search local IP'''
    logging.info("search for IP")
    logging.debug(line)
    result = line.find('169.254')
    items=re.findall("^.*169.254.*$",line,re.MULTILINE)
    if result == -1:
        found = False
    else:
        found =True
    ipexists = {
        "ipstate": found,
        "ipaddress": items
    }
    return ipexists
