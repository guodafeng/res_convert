#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import re
import logging
import argparse
from openpyxl import Workbook
import collections


import constants
import utility 
import picksource
#
xlsx1 = 'string_src/diff/Souce template-example.xlsx'
xlsx2 = 'string_src/diff/kaios_update.xlsx'
src_map1 = picksource.SourceToXlsx.load_source_xlsx(xlsx1)
src_map2 = picksource.SourceToXlsx.load_source_xlsx(xlsx2)

diff1 = []
for key in src_map1:
    if key not in src_map2:
        diff1.append(src_map1[key])

diff2 = []
for key in src_map2:
    if key not in src_map1:
        diff2.append(src_map2[key])


picksource.SourceToXlsx.save_source_xlsx(diff1, 'diff1.xlsx')
picksource.SourceToXlsx.save_source_xlsx(diff2, 'diff2.xlsx')

