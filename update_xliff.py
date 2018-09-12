import sys
import os
import re
import logging
import xml.etree.ElementTree as ET

import utility
import map_t2_string
from dbwrapper import *

def load_sourcebase(source_tb='tb_source.txt'):
    """
    create textid to sourcebaseid map
    """
    pattern = re.compile(r'(\S+)\s+(\S+)\s+(\S+)')

    lines = utility.read_as_list(source_tb)
    sourcebase_map = {}

    for line in lines:
        match = pattern.search(line)
        if match:
            textid = match.groups()[2]
            sourcebaseid = match.groups()[1]
            sourcebase_map[textid] = sourcebaseid
    return sourcebase_map


def load_targetbase(tr_tb='tb_tr.txt'):
    """
    create (sourcebaseid, lang_id) to target base id map
    """
    pattern = re.compile(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')

    lines = utility.read_as_list(tr_tb)
    targetbase_map = {}

    for line in lines:
        match = pattern.search(line)
        if match:
            baseid = match.groups()[1]
            lang_id = match.groups()[2]
            sourcebaseid = match.groups()[3]
            targetbase_map[(sourcebaseid, lang_id)] = baseid
    return targetbase_map


   
def load_langmap(lang_tb = 'tb_lang.txt'):
    """
    create lang code to lang id map
     """
    pattern = re.compile(r'(\S+)\s+.+\s+(\S+)')

    lines = utility.read_as_list(lang_tb)
    lang_map = {}

    for line in lines:
        match = pattern.search(line)
        if match:
            lang_code = match.groups()[1]
            lang_id = match.groups()[0]
            lang_map[lang_code] = lang_id
    return lang_map


def update_xliff(folder):
    t2_map, old_map = map_t2_string.load_t2_source(map_source_table())
    sourcebase_map = load_sourcebase()
    targetbase_map = load_targetbase()
    lang_map = load_langmap()

    def is_xliff(name):
        return name[-4:] == '.xlf' or name[-6:] == '.xliff'

    skipped = set()
    kept = set()
    newid_skipped = set()
    folder = os.path.abspath(folder)
    for item in os.listdir(folder):
        subpath = os.path.join(folder, item)
        if os.path.isfile(subpath) and is_xliff(subpath):
            print(subpath)
            xliff_update = XliffUpdate(subpath, old_map, sourcebase_map,
                    targetbase_map, lang_map)
            xliff_update.do_update_raw()
            skipped.update(xliff_update.skipped)
            kept.update(xliff_update.valids)
            newid_skipped.update(xliff_update.newid_skipped)
    utility.save_list(os.path.join(folder,'not_in_t2_oldid.txt'), '\r\n'.join(skipped))
    utility.save_list(os.path.join(folder,'not_in_db_newid.txt'),
            '\r\n'.join(newid_skipped))
    utility.save_list(os.path.join(folder,'kept.txt'), '\r\n'.join(kept))


class XliffUpdate(object):
    """
    only support product-version=2.2 and 2.1
    """
    IDLE_S = 0
    PROCESSING_S = 1
    SKIP_S = 2 
    def __init__(self, xliff, old_map, source_base_map, base_map,
            lang_map):
        self.xliff = xliff

        self.old_map = old_map
        self.source_base_map = source_base_map
        self.base_map = base_map
        self.lang_map = lang_map
        self.new_account = 'KAIOS_UPDATE'
        self.skipped = []
        self.newid_skipped = []
        self.valids = []
        self.skipline = False
        self.version = None


    def do_update_raw(self):
        target_lan = None

        lines = utility.read_as_list(self.xliff)
        out_lines = []

        def parse_target_lan(line):
            match = re.search(r'target-language="([^"]+)"', line)
            if match:
                return match.groups()[0]

        def parse_version(line):
            match = re.search(r'product-version="([^"]+)"', line)
            if match:
                return match.groups()[0]

        def parse_in_group(line):
            match = re.match(r'\s*<group.+>', line)
            return True if match else False

        def is_end_group_tag(line):
            match = re.match(r'\s*</group>', line)
            return True if match else False


        for line in lines:
            if not target_lan:
                target_lan = parse_target_lan(line)
                if target_lan:
                    self.lang_id = self.lang_map[target_lan]

            if not self.version:
                self.version = parse_version(line)

            line = self._update_group_raw(line)

            if not self.skipline:
                out_lines.append(line)

            if is_end_group_tag(line):
                self.skipline = False

        utility.save_list(self.xliff, out_lines)


    def _update_attrib(self, line, attrib, value):
        pattern = r'{0}=[^;"]*'.format(attrib)
        rep = '{0}={1}'.format(attrib, value)
        line = re.sub(pattern, rep, line)
        return line

    def _update_outattrib(self, line, attrib, value):
        pattern = r'{0}="[^"]+"'.format(attrib)
        rep = '{0}={1}'.format(attrib, value)
        line = re.sub(pattern, rep, line)
        return line
 
    def _get_id_tag(self):
        if self.version == '2.2':
            return 'resname'
        elif self.version == '2.1':
            return 'id'

    def _update_resname(self, line):
        def get_resname(line):
            pattern = \
                re.compile(r'{0}="([^"]+)"'.format(self._get_id_tag()))

            match = pattern.search(line)
            if match:
                return match.groups()[0]
        # all group info should use same new account, otherwise error
        # when import to DB
        line = self._update_attrib(line, 'x-account', self.new_account)
        resname = get_resname(line)
        if resname not in self.old_map: 
            # skip if the resname is not in t2 string table
            print("not in old_map, skipped resname:", resname)
            self.skipped.append(resname)
            self.skipline = True
            return line

        t2_item = self.old_map[resname]
        self.new_res_id = t2_item.textid
        self.new_feature = t2_item.feature

        if self.new_res_id not in self.source_base_map:
            print("new_res_id:", self.new_res_id)
            print("not in source_base_map, skipped resname:", resname)
            self.newid_skipped.append(self.new_res_id)
            self.skipline = True
            return line

        self.new_sourcebaseid = self.source_base_map[self.new_res_id]
        self.new_targetbaseid = self._get_targetbase(self.new_sourcebaseid,
                self.lang_id)
        line = self._update_outattrib(line, self._get_id_tag(),
                '"{0}"'.format(self.new_res_id))
        line = self._update_attrib(line, 'x-feature', self.new_feature)
        line = self._update_attrib(line, 'x-sourceid',
                self.new_sourcebaseid)
        line = self._update_attrib(line, 'x-sourcebaseid',
                self.new_sourcebaseid)

        self.valids.append(self.new_res_id)
        return line

    def _update_transunit(self, line):
        if self.skipline:
            return line

        line = self._update_attrib(line, 'x-targetid',
                self.new_targetbaseid)
        line = self._update_attrib(line, 'x-targetbaseid',
                self.new_targetbaseid)

        return line
    
    def _update_context_group(self, line):
        if self.skipline or self.version == '2.1':
            return line
        line = self._update_outattrib(line, 'name',
                '"{0}"'.format(self.new_res_id))
        return line


    def _update_group_raw(self, line):
        def is_group_tag(line):
            match = re.match(r'\s*<group.+>', line)
            return True if match else False

        def is_trans_unit(line):
            match = re.match(r'\s*<trans-unit.+>', line)
            return True if match else False

        def is_context_group(line):
            match = re.match(r'\s*<context-group.+>', line)
            return True if match else False

        if is_group_tag(line):
            line = self._update_resname(line)
        elif is_trans_unit(line):
            line = self._update_transunit(line)
        elif is_context_group(line):
            line = self._update_context_group(line)

        return line

    def _get_sourcebase(self, textid):
        return self.source_base_map[textid]

    def _get_targetbase(self, sourcebaseid, lang_id):
        return self.base_map[(sourcebaseid, lang_id)]

       
def map_source_table():
    # return 'map_source_t2_v3.xlsx'
    return 'string_src/translation/newfeatureidmap2.xlsx'



def load_id_map(xlsx):
    """
     type: xlsx file contains two column, column 0 is old id, column 1
        is new id
     rtype: old id -> new id map
    """
    from openpyxl import load_workbook
    wb = load_workbook(filename = xlsx)
    ws = wb.active
    rows = ws.rows
   
    id_map = {}
    for row in rows:
        id_map[row[0].value] = row[1].value

    return id_map

def load_sourcebase_db(ids):
    whereClause = WhereClause()
    whereClause.add('textid', ids)
    dbWrapper = DBWrapper()
    return dbWrapper.select_sourcebase(whereClause.clauses)

def load_tr_db(ids):
    whereClause = WhereClause()
    whereClause.add('sourcebase_id', ids)
    dbWrapper = DBWrapper()
    return dbWrapper.select_tr(whereClause.clauses)


def is_xliff(name):
    return name[-4:] == '.xlf' or name[-6:] == '.xliff'

def all_xliff_infolder(folder):
    folder = os.path.abspath(folder)
    for item in os.listdir(folder):
        subpath = os.path.join(folder, item)
        if os.path.isdir(subpath):
            yield from all_xliff_infolder(subpath)
        if os.path.isfile(subpath) and is_xliff(subpath):
            yield subpath
 
def update_xliff_new(folder):
    t2_map, old_map = map_t2_string.load_t2_source(map_source_table())
    print(t2_map)
    print(old_map)
    sourcebase_map = load_sourcebase_db(t2_map.keys())
    print(sourcebase_map)
    tr_map = load_tr_db(sourcebase_map.values())
    lang_map = DBWrapper().select_languages_as_map()

    skipped = set()
    kept = set()
    newid_skipped = set()

    for xliff_file in all_xliff_infolder(folder):
        xliff_update = XliffUpdate(xliff_file, old_map, sourcebase_map,
                    tr_map, lang_map)
        xliff_update.do_update_raw()
        skipped.update(xliff_update.skipped)
        kept.update(xliff_update.valids)
        newid_skipped.update(xliff_update.newid_skipped)

    utility.save_list(os.path.join(folder,'not_in_t2_oldid.txt'), '\r\n'.join(skipped))
    utility.save_list(os.path.join(folder,'not_in_db_newid.txt'),
            '\r\n'.join(newid_skipped))
    utility.save_list(os.path.join(folder,'kept.txt'), '\r\n'.join(kept))



#test()
# update_xliff('string_src/xliff/Batch2')
# update_xliff('string_src/xliff/Batch3')
# update_xliff('string_src/xliff/Batch4')
# update_xliff('string_src/xliff/Batch5')
# update_xliff('string_src/xliff/Batch6')
# update_xliff('string_src/xliff/Batch7')


update_xliff_new('string_src/translation/legal')



