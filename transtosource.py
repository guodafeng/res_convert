#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re
import logging
import argparse
from openpyxl import Workbook
from collections import defaultdict
from openpyxl import load_workbook

import constants
import utility 
import picksource

g_logger = None
def mylogger():
    global g_logger
    if g_logger is None:
        g_logger = get_logger()

    return g_logger
 
class TranslateItem(object):
    def __init__(self, account, project, feature, textid, langcode,
            translation):
        self.account = account
        self.project = project
        self.feature = feature
        self.textid = textid
        self.langcode = langcode
        self.translation = translation

class XlsxToSource(object):
    """
    transfer xlsx back to .property files, group translated different 
    languages to different folder
    """
    def load_translate_xlsx(self, xlsx):
        """
        group the translation in xlsx by langcode
        return dict
        """

        wb = load_workbook(filename = xlsx)
        ws = wb.active
        rows = ws.rows

        #index + 1 because the contents started from 2nd column
        col_map = {name:index+1 for index, name in \
                enumerate(constants.TRANSLATIONS_COLUMNS)}
        
        idx = col_map[constants.TEXTID]
        translations = []

        for num, row in enumerate(rows):
            if num < constants.TITLE_ROW:
                continue

            acc_idx = col_map[constants.ACCOUNT]
            prj_idx = col_map[constants.PROJECT]
            fea_idx = col_map[constants.FEATURE] 
            lan_idx = col_map[constants.LANGCODE]
            tran_idx = col_map[constants.TRANSLATION]

            trans_item = \
            TranslateItem(row[acc_idx].value, row[prj_idx].value, 
                row[fea_idx].value, row[idx].value, row[lan_idx].value, 
                row[tran_idx].value) 

            translations.append(trans_item)
            idx = col_map[constants.TEXTID]

        return translations

    def _get_lancode_map(self, translations):
        lancode_map = defaultdict(list)
        for trans in translations:
            lancode_map[trans.langcode].append(trans)

        return lancode_map

    def _get_id_map(self, translations):
        id_map = defaultdict(list)
        for trans in translations:
            id_map[trans.textid].append(trans)

        return id_map

    def update_t2_with_trans(self, t2_xlsx, trans_xlsx):
        translations = self.load_translate_xlsx(trans_xlsx)
        id_map = self._get_id_map(translations)

        wb = load_workbook(filename = t2_xlsx)
        ws = wb.get_sheet_by_name('MESSAGE')
        
        rows = ws.rows
        col_map = {name:index for index, name in enumerate(T2_COL_NAME)}
        for row in rows:
            textid = row[col_map[ID_TITLE]].value
            if textid in id_map:
                trans_of_id = id_map[textid]
                for trans in trans_of_id:
                    #todo:not finished yet
                    pass
                
            
    def save_trans_t2(self, trans_xlsx, t2_xlsx):
        translations = self.load_translate_xlsx(trans_xlsx)
        id_map = self._get_id_map(translations)
        lancode_map = self._get_lancode_map(translations)

        wb = Workbook()
        ws = wb.active

        # create map from langcode to column index in xlsx
        # fill title row 
        cur_row = 1
        cur_col = 1
        ws.cell(row=cur_row, column=cur_col).value = 'RefName' 
        col_map = {'RefName':cur_col}
        for code in sorted(lancode_map.keys()):
            cur_col += 1
            ws.cell(row=cur_row, column=cur_col).value = code
            col_map[code] = cur_col 

        # fill translation row
        for textid in sorted(id_map.keys()):
            cur_row += 1
            cur_col = col_map['RefName']
            ws.cell(row=cur_row, column=cur_col).value = textid
            for trans in id_map[textid]:
                cur_col = col_map[trans.langcode]
                ws.cell(row=cur_row, column=cur_col).value = trans.translation

        wb.save(t2_xlsx)

    def trans_to_source(self, source_us, source_xlsx, trans_xlsx):
        """
        for each langcode in trans_xlsx, copy source_us to langcode
            named folder, and update the .properties files according to
            source_xlsx and trans_xlsx
        """
        import copy
        import shutil

        source_map = picksource.SourceToXlsx.load_source_xlsx(source_xlsx)
        translations = self.load_translate_xlsx(trans_xlsx)
        lancode_map = self._get_lancode_map(translations)

        source_root = os.path.abspath(os.path.join(source_us, os.pardir))
        for lancode in lancode_map:
            source_lan = os.path.join(source_root, lancode)

            if not os.path.exists(source_lan):
                shutil.copytree(source_us, source_lan)

            # map source file and all it's translate string
            trans_source_map = defaultdict(list)
            for tran in lancode_map[lancode]:
                src_item = source_map[tran.textid]
                tran_src_item = copy.copy(src_item)
                tran_src_item.value = tran.translation
                trans_source_map[tran_src_item.res_file].append(tran_src_item)

            self.update_source_lan(source_lan, trans_source_map)


    def update_source_lan(self, source_lan, source_map):
        for relpath in source_map:
            picksource.SourceUpdate().update_file(os.path.join(source_lan,
                relpath), source_map[relpath])


def to_t2_xlsx_main():
    parser = argparse.ArgumentParser(description='Create excel file\
            with translation filled in t2 format')

    parser.add_argument('-i','--in', nargs='+', 
                       help='translation table exported from \
                       nstring')
    parser.add_argument('-o','--out', nargs='+', 
                      help='output file. translation table in t2 \
                      format')
    args = vars(parser.parse_args())
    nstring_trans = 'string_src/trans.xlsx'
    t2_trans = 'string_src/trans_t2.xlsx'
    if args['in']:
        nstring_trans = args['in'][0]
    if args['out']:
        t2_trans = args['out'][0]

    convertor = XlsxToSource()
    convertor.save_trans_t2(nstring_trans, t2_trans)

def to_source_file_main():

    parser = argparse.ArgumentParser(description='Create translated \
    source files from base source files.')

    parser.add_argument('-b','--base', nargs='+', required=True,
                       help='''Define root path of resource files.
                       Normally it is the path of en-US folder.''')

    parser.add_argument('-s','--sourcetable', nargs='+', 
                       help='''The source table (xlsx file) generated 
                       from base source files. If not given, it will be
                       set to source.xlsx which has the same parent with
                       path set by --base''')

    parser.add_argument('-t','--translationtable', nargs='+',
                       help='''The translation table (xlsx file) which
                       contains the translated string. The translation
                       will be update to source file according the ID
                       mapping in source table.''')
   
    args = vars(parser.parse_args())
   
    source_base = args['base'][0]
    parent = os.path.abspath(os.path.join(source_base, os.pardir))

    if args['sourcetable']:
        source_table = args['sourcetable'][0]
    else:
        source_table = os.path.join(parent, 'source.xlsx')

    if args['translationtable']:
        trans_table = args['translationtable'][0]
    else:
        trans_table = os.path.join(parent, 'trans.xlsx')

    convertor = XlsxToSource()
    convertor.trans_to_source(source_base, source_table, trans_table)

if __name__ == '__main__':
    to_t2_xlsx_main()

