import pymssql

import utility


server = 'BJ-SQL02.fihtdc.com'
user='nString'
password='Nstring123456'

with pymssql.connect(server, user, password, 'nstring',charset='utf8')\
as conn:
    with conn.cursor(as_dict=False) as cursor:
        textids = "('communications:contacts:contacts:email',\
            'communications:contacts:contacts:imported',\
            'communications:contacts:contacts:notImported',\
            'settings:settings:bluetooth',\
            'settings:settings:feedback-attention',\
            'settings:settings:feedback-contactrequest',\
            'settings:settings:feedback-contactyou',\
            'settings:settings:feedback-givescore',\
            'settings:settings:feedback-likely',\
            'settings:settings:feedback-mood-explain',\
            'settings:settings:feedback-notlikely',\
            'settings:settings:feedback-sending',\
            'settings:settings:insert-sim',\
            'settings:settings:skip',\
            'system:system:bluetoothButton-off',\
            'system:system:bluetoothButton-on',\
            'system:system:power',\
            'system:system:powerconfirm')"

        sql = "select Text, Account, Project, Feature, Language, Lv1 \
        from TranslationView where Account='KAIOS_UPDATE' and Text in " \
        + textids

        cursor.execute(sql)


        lines = []
        for index, row in enumerate(cursor):
            line = '    '.join(row)
            line = line.replace('\n','')
            line = line.replace('\r','')

            line += '\n'
            lines.append(line)
            

        utility.save_list('tb_searched.txt', lines)




