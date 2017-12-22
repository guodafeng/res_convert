#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re
from collections import defaultdict
from collections import namedtuple
import pymssql

server = 'BJ-SQL02.fihtdc.com'
user='nString'
password='Nstring123456'

class WhereClause(object):
    def __init__(self):
        self.clauses = ''

    def add(self, field, values):
        if len(values)<=0: # do nothing empty values
            return

        clause = '{0} IN ({1})'.format(field, ', '.join(map(repr,values)))


        if self.clauses:
            self.clauses = ' {0} AND {1}'.format(self.clauses, clause)
        else:
            self.clauses = ' WHERE {0}'.format(clause)


Account = namedtuple('Account', ['id', 'name'])

class DBWrapper(object):
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = pymssql.connect(server, user, password, 
                'nstring',charset='utf8')
    def close(self):
        self.conn.close()

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.close()

    def select_translation(self, where_clause):
        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select Text, Account, Project, Feature, Language, Lv1 \
            from TranslationView" + where_clause

            cursor.execute(sql)

            lines = []
            translations = []
            for row in cursor:
                trans_item = \
                TranslateItem(row['Account'], row['Project'],
                row['Feature'],row['Text'], row['Language'],
                row['Lv1'])

                translations.append(trans_item)

            return translations

    def select_account(self):
        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select id, name from Customer"
            cursor.execute(sql)

            accounts = []
            for row in cursor:
                accounts.append(Account(row['id'],row['name']))

            return accounts

    def select_languages_as_map(self):
        '''rtype: code -> id map
        '''
        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select id, name, code from Language"
            cursor.execute(sql)

            lang_map = {}
        
            for row in cursor:
                lang_map[row['code']] = row['id']

            return lang_map

    def select_sourcebase(self, where_clause):
        '''rtype: textid -> base id map
        '''

        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select baseid, textid from Source" + where_clause
            cursor.execute(sql)

            source_map = {}
            for row in cursor:
                source_map[row['textid']] = row['baseid']

            return source_map

    def select_tr(self, where_clause):
        '''rtype: textid -> base id map
        '''

        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select baseid, language_id, sourcebase_id from TR"\
                    + where_clause
            cursor.execute(sql)

            ret = {}
            for row in cursor:
                ret[(row['sourcebase_id'],row['language_id'])] =\
                        row['baseid']

            return ret



  
    def select_language(self, account_id):
        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select Language from ViewLanguageSetLanguage" + \
                    " where account_id=" + str(account_id)
            cursor.execute(sql)

            langs = []
            for row in cursor:
                langs.append(row['Language'])

            return langs

    def select_project(self, account_id):
        with self.conn.cursor(as_dict=True) as cursor:
            sql = "select name from Project where account_id =" + \
            str(account_id)
            
            cursor.execute(sql)

            projects = []
            for row in cursor:
                projects.append(row['name'])

            return projects




