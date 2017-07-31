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






