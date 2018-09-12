import sys
import os
import re
import logging
import argparse
from openpyxl import Workbook
from collections import defaultdict
from openpyxl import load_workbook


ROW_HEAD = 0
COL_PATH = 0
COL_FNAME = 1
COL_ID = 2
PROP_RT = '/home/data/yf/kai_india2/gaia/distribution/locales/'

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

        # language code column map, {lang: column}
        lang_col = {}
        # lang code to text string map
        # {lang: {relpath: {textID: text} }}
        lang_strings = {}
        
        for rownum, row in enumerate(rows):
            if rownum == ROW_HEAD:
                for idx, cell in enumerate(row):
                    if idx > COL_ID and cell.value:
                        lang_col[cell.value] = idx
                        lang_strings[cell.value] = {}
                # print(lang_col)
            else:
                relpath = row[COL_PATH].value + '/' + \
                    row[COL_FNAME].value + '.properties'
                textID = row[COL_ID].value

                for lang in lang_col:
                    if relpath not in lang_strings[lang]:
                        lang_strings[lang][relpath] = {}
                    file_strings = lang_strings[lang][relpath]
                    textCol = lang_col[lang]
                    file_strings[textID] = row[textCol].value
        # print(lang_strings)
        return lang_strings

        
    def update_properties(self, lang_strings):
        for lang, strings in lang_strings.items():
            for relpath, file_strings in strings.items():
                self.update_one_property(lang + relpath, file_strings)
        pass


    def update_one_property(self, prop_file, file_strings):
        """
        file_strings: {textID: text,...}
        prop_file: properties file to be update
        """
        #to match name = value in file except start with #
        prog = re.compile(r'^\s*(?!#)\s*([^= ]+)\s*=\s*(.*)\s*')
        
        out_lines = []
        fullpath = PROP_RT + prop_file 
        text_updated = False
        text_added = False

        if not os.path.exists(fullpath):
            print("No properties file", fullpath, sep=':')
            return
            
        with open(fullpath) as f:
            for line in f:
                m = prog.match(line)
                if m:
                    f_id = m.groups()[0].strip()
                    f_text = m.groups()[1].strip()
                    if f_id in file_strings:
                        x_text = file_strings.pop(f_id)
                        if x_text and f_text != x_text:
                            # the text is different in .properties file
                            # compared to .xlsx file, use text from xlsx
                            print('updated:', prop_file, f_id, f_text, x_text, sep=':')
                            line = f_id + "=" + x_text + "\n"
                            text_updated = True
                out_lines.append(line)
            for x_id, x_text in file_strings.items():
                text_added = True
                if x_text:
                    newline = x_id + "=" + str(x_text) + "\n"
                    print("new added", prop_file, newline, sep=':')
                    out_lines.append(newline)

        # save new content
        with open(fullpath, 'w', encoding='utf-8') as fw:
            fw.writelines(out_lines)
            print(out_lines)
        

    def check_tranlation(self, xlsx):
        lang_strings = self.load_translate_xlsx(xlsx)
        self.update_properties(lang_strings)



if __name__ == '__main__':
    convertor = XlsxToSource()
    convertor.check_tranlation('/home/yunfeng/dev/indian_patch/india.xlsx')


