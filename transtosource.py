#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re
import logging
import argparse
from openpyxl import Workbook


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
        from openpyxl import load_workbook
        from collections import defaultdict

        wb = load_workbook(filename = xlsx)
        ws = wb.active
        col_map = constants.col_in_xlsx(constants.TRANSLATIONS_COLUMNS,
                start = 'B')
        read_row = constants.TITLE_ROW + 1
        
        idx = col_map[constants.TEXTID] + str(read_row)
        translate_map = defaultdict(list)
        while ws[idx].value is not None:
            acc_idx = col_map[constants.ACCOUNT] + str(read_row)
            prj_idx = col_map[constants.PROJECT] + str(read_row)
            fea_idx = col_map[constants.FEATURE] + str(read_row)
            lan_idx = col_map[constants.LANGCODE] + str(read_row)
            tran_idx = col_map[constants.TRANSLATION] + str(read_row)

            translate_map[ws[lan_idx].value].append(
            TranslateItem(ws[acc_idx].value, ws[prj_idx].value, 
                ws[fea_idx].value, ws[idx].value, ws[lan_idx].value, 
                ws[tran_idx].value) )

            read_row += 1 
            idx = col_map[constants.TEXTID] + str(read_row)

        return translate_map

    def trans_to_source(self, source_us, source_xlsx, trans_xlsx):
        """
        for each langcode in trans_xlsx, copy source_us to langcode
            named folder, and update the .properties files according to
            source_xlsx and trans_xlsx
        """
        from collections import defaultdict
        import copy
        source_map = SourceToXlsx.load_source_xlsx(source_xlsx)
        trans_map = self.load_translate_xlsx(trans_xlsx)

        source_root = os.path.abspath(os.path.join(source_us, os.pardir))
        for lancode in trans_map:
            source_lan = source_root + '\\' + lancode
            if not os.path.exists(source_lan):
                os.mkdir(source_lan)

            # map source file and all it's translate string
            trans_source_map = defaultdict(list)
            for tran in trans_map[lancode]:
                src_item = source_map[tran.textid]
                tran_src_item = copy.copy(src_item)
                tran_src_item.value = tran.translation
                trans_source_map[tran_src_item.res_file] = tran_src_item

            update_source_lan(source_lan, trans_source_map)

    def update_source_lan(source_lan, source_map):
        for relpath in source_map:
            update_file(source_lan + '\\' + relpath,
                    source_map[relpath])

    def update_file(source_file, res_list):






