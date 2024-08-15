# coding: utf-8
# boxdrowings.csv を characters.dic 形式に変換して UTF-8 で print する

import csv
import unicodedata

CSV_FILE = "boxdrowings.csv"
CONSOLE_ENCODING = 'utf-8' #'mbcs'

def my_print(s):
	print(s.encode(CONSOLE_ENCODING, 'ignore'))

def utf8_decode_fields(fields):
    ar = []
    for f in fields:
        ar.append(unicodedata.normalize('NFKC', f.decode('utf-8')))
    return ar

items = []
for fields in csv.reader(open(CSV_FILE)):
	ch, jname, lname, sname, uname, mspt, ucpt = utf8_decode_fields(fields)
	if ch == '罫線': continue  # noqa: E701
	items.append([ch, ucpt[2:], sname, lname])

for i in sorted(items, key=lambda i: i[1]):
	my_print('\t'.join([i[0], i[1].lower(), "[%s]" % i[2], i[3]]))
