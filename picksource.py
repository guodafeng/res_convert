#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import re
import logging
import constants
import argparse
import uuid

from collections import defaultdict
from utility import *



g_logger = None
g_root = ""

# 1. pick id and values from .property file to xlsx
# 2. transfer xlsx back to .property files, group translated different 
#    languages to different folder
class SourceItem(object):
    uni_ids = set()

    def __init__(self, name, value, res_file):
        self.name = name
        self.value = value
        self.res_file = res_file
        self.uni_name = name + '_' + self.get_uniq_id()

    def get_uniq_id(self):
        uni_id = str(uuid.uuid4())[:8]
        while uni_id in SourceItem.uni_ids:
            g_logger.warn(uni_id + 'id collision, reproduce')
            uni_id = str(uuid.uuid4())[:8]
        SourceItem.uni_ids.add(uni_id)
        return uni_id


    def __repr__(self):
        return '%s, %s, %s, %s' % (self.uni_name, self.name, self.value, self.res_file)

def pick_res(root):
    res_list = []  #store all matched "name = value"
    
    g_logger.info("Picking folder:" + root)
    for item in os.listdir(root):
        path = os.path.join(root, item)
        if os.path.isdir(path):
            res_list += pick_res(path)
        elif _is_res_file(path):
            res_list += pick_res_file(path)

        else:
            g_logger.debug('Skipped file: ' + path)
    return res_list

def save_to_xlsx(res_list):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active

    ws['A1'] = 'Generated from folder %s' % g_root
    
    #add title row
    col_num = ord('A')
    row_num = str(constants.TITLE_ROW)
    for col in constants.MANDATORYSOURCES_COLUMNS:
        cell = chr(col_num) + row_num
        ws[cell] = col
        col_num += 1

    for res in res_list:


    wb.save('test.xlsx')




def print_duplicate(res_list):
    names_dict = defaultdict(list) 
    for res in res_list:
        names_dict[res.name].append(res)

    for key in names_dict:
        if len(names_dict[key]) > 1:
            temp = names_dict[key]
            value = temp[0].value
            duplicated = str(temp[0])
            for t in temp:
                if t.value != value:
                    duplicated += ('\n' + str(t))
                    
            if duplicated != str(temp[0]):
                print( duplicated)


def get_res_pattern():
    #re.compile(r'([a-zA-Z0-9_\-\.\[\]]*)\s*=\s*(.*)')
    return re.compile(r'([^=]+)\s*=\s*(.*)')

def get_comment_pattern():
    return re.compile(r'^\s*#.*')

def pick_res_file(file_name):
    """
    file_name: the file name of .propery file
    output: [SourceItem()] of the property file
    """
    g_logger.info("Picking file:" + file_name)

    pair = get_res_pattern()
    comment = get_comment_pattern()

    lines = read_as_list(file_name)

    relative_path = os.path.relpath(file_name, g_root)
    res_list = []
    comments = []
    mismatchs = []
    for line in lines:
        if comment.match(line):
            comments.append(line)
            continue
        if line.strip() == '':
            continue # skip blank lines
        
        match = pair.match(line)
        if match:
            res_list.append(SourceItem(match.groups()[0].strip(),
                match.groups()[1].strip(),
                relative_path))
        else:
            mismatchs.append(line)

    if len(mismatchs) > 0:
        g_logger.warn('In %s mismatched lines:\n %s' % (file_name,
            ''.join(mismatchs)))
    g_logger.debug('In %s commented lines:\n %s' % (file_name, 
        ''.join(comments)))

    return res_list
    
def _is_res_file(file_name):
    name_split = os.path.splitext(os.path.basename(file_name))
    if name_split[0] in ['manifest']:
        return False
    if name_split[1] != '.properties':
        return False
    return True
    
def process_res(root):
    global g_root
    global g_logger

    g_root = root
     # prepare_out_folder
    parent = os.path.abspath(os.path.join(g_root,
        os.pardir))
    out_folder = os.path.join(parent, 'res_pick')
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # set all output to out_folder
    print("change out dir to:" + out_folder)
    os.chdir(out_folder)

    g_logger = get_logger()

    try:
        res_list = pick_res(g_root)
        save_to_xlsx(res_list)
        
    except Exception as e:
        g_logger.error(str(e))
        pass
 
def main():
    parser = argparse.ArgumentParser(valueription='Pick resource string \
    from given folder')

    parser.add_argument('-i','--in', nargs='+', required=True,
                       help='''Define root folder of resource files. It is mandatory.''')

    parser.add_argument('-o', '--out', nargs='+',
                        help='''The result output folder, including log
                        files''')
    
    args = vars(parser.parse_args())
   
    process_res(os.path.abspath(args['in'][0]))

def main_test():
    line = 'simContacts-imported3[two]    = Imported {{n}} contacts'
    pair = re.compile(r'([a-zA-Z0-9_\-\.]*)\s*=\s*(.*)')
    match = pair.match(line)
    if match:
        print(match.group()) 
    else:
        print('cannot match: ' +line)

    #call_pick_res('en-GB')
    
   

if __name__ == '__main__':
    main()

