import os
import logging
import sys
import re
import __main__

#utility funcionts
def read_as_list(file_name):
    fh = open(file_name, 'r', encoding='utf8')
    lines = fh.readlines()
    fh.close()
    return lines

def read_all(file_name):
    fh = open(file_name, 'r', encoding='utf8')
    lines = fh.read()
    fh.close()
    return lines


def save_list(filename, lines, param = 'w'):
    fh = open(filename, param, encoding='utf8')
    fh.writelines(lines)
    fh.close()

def set_path_to_current_file():
    os.chdir(os.path.realpath(os.path.dirname(__main__.__file__)))

def replace_separator(path):
    """
    path: the path might be windows or unix separated
    out: change to system related separator
    """
    if path:
        sep = r'[/\\]'
        elms = re.split(sep, path)
        return os.path.join(*elms)




def get_module():
    #(__main__.__file__): filename of the script calling this function
    #(__file__): current file name
    return os.path.splitext(os.path.basename(__main__.__file__))[0]

def get_logger(path=''):
    if path == '':
        path = os.path.dirname(__main__.__file__)

    module_name = get_module()
    logfile = os.path.join(path, module_name + '.log')
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(logfile, encoding='utf8')
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    #formatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)s -"
            #" %(funcName)20s() ] %(message)s")
    formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    mylog = get_logger()
    mylog.info("just a test")


