# -*- coding: utf-8 -*-


def alpha2mb(s):
	# 'abc' -> 'ａｂｃ'
	from_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	to_table = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
	result = ""
	for ch in s:
		pos = from_table.find(ch)
		if pos >= 0:
			result += to_table[pos]
	return result
