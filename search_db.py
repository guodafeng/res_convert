import pymssql

import utility


def get_textids(fname = 'string_src/textids.txt'):
    with open(fname,'r',encoding='utf8') as f:
        textids="("
        for line in f.readlines():
            line = line.strip()
            if line:
                textids = "{0}'{1}',".format(textids, line)
        textids = textids[:-1]  + ")"#remove last comma

    return textids



server = 'BJ-SQL02.fihtdc.com'
user='nString'
password='Nstring123456'

with pymssql.connect(server, user, password, 'nstring',charset='utf8')\
as conn:
    with conn.cursor(as_dict=False) as cursor:
        textids = get_textids()

        sql = "select Text, Account, Project, Feature, Language, Lv1 \
        from TranslationView where Account='KAIOS_UPDATE' and Text in " \
        + textids

        print(sql)
        cursor.execute(sql)


        lines = []
        for index, row in enumerate(cursor):
            line = '    '.join(row)
            line = line.replace('\n','')
            line = line.replace('\r','')

            line += '\n'
            lines.append(line)
            

        utility.save_list('tb_searched.txt', lines)




