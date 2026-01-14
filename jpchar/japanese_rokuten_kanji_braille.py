# coding: UTF-8
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017 Takuya Nishimoto (NVDA Japanese Team)

SRC_FILE = "6ten kanji characters table-UTF8.txt"

with open(SRC_FILE, encoding="utf-8-sig") as f:
	for s in f.readlines():
		if s and s[0] != "#":
			s = s.strip('"\n')
			a = s.split("\t")
			if len(a) == 2:
				print(f"sign \\x{ord(a[0]):x}  {a[1]:<20}\t# {a[0]}")
