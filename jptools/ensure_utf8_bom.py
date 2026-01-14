# coding: UTF-8
# Usage:
# > python jptools\ensure_utf8_bom.py include\espeak\src\libespeak-ng\tr_languages.c

import sys
import codecs

if __name__ == "__main__":
	fileName = sys.argv[1]
	print(fileName)
	if codecs.open(fileName, "r", "utf_8", errors="replace").readline()[0] == "\ufeff":
		print("with bom")
	else:
		print("without bom")
		with codecs.open(fileName, "r", "utf_8", errors="replace") as f:
			data = f.read()
		with codecs.open(fileName, "w", "utf_8_sig", errors="replace") as f:
			f.write(data)
		print("converted to utf8 with bom")
