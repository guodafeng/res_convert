import os
import logging
import sys
import __main__

#utility funcionts
def read_as_list(file_name):
    fh = open(file_name, 'r', encoding='utf8')
    lines = fh.readlines()
    fh.close()
    return lines

def get_module():
    #(__main__.__file__): filename of the script calling it
    #(__file__): current file name
    return os.path.splitext(os.path.basename(__main__.__file__))[0]

def get_logger():
    module_name = get_module()
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(module_name + '.log', encoding='utf8')
    fh.setLevel(logging.WARN)
    #fh.setLevel(logging.ERROR)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
