# coding: UTF-8
# compareSymbolsDic.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015 Takuya Nishimoto (NVDA Japanese Team)

import codecs

import _checkCharDesc as cd

en_sym_file = r"..\..\srt\ja\symbols-newRevisions\11146\symbols.dic"
ja_sym_file = r"..\..\srt\ja\symbols.dic"

en_syms, en_src = cd.read_symbol_file(en_sym_file, returnSource=True)
ja_syms, ja_src = cd.read_symbol_file(ja_sym_file, returnSource=True)

# pprint.pprint(en_syms)
with codecs.open("__output", "w", "utf-8") as wf:
	for k, v in sorted(en_syms.items()):
		ja = ja_syms.get(k)
		ordk = ord(k[0])
		if ordk <= 0x001F:
			k = ""
		if ja is not None:
			wf.write("o U+%04x (%s) e:%d (%s) j:%d (%s)\n" % (ordk, k, v[0], v[1], ja[0], ja[1]))
		else:
			wf.write("x U+%04x (%s) e:%d (%s)\n" % (ordk, k, v[0], v[1]))
